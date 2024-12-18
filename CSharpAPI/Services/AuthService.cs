using CSharpAPI.Data;
using Microsoft.EntityFrameworkCore;

namespace CSharpAPI.Services
{
    public interface IAuthService
    {
        Task<bool> HasAccess(string role, int? warehouseId, string resource, string method);
    }

    public class AuthService : IAuthService
    {
        private readonly SQLiteDatabase _context;
        private readonly HashSet<string> _warehouseSpecificRoles = new()
        {
            "warehousemanager",
            "inventorymanager",
            "floormanager",
            "operative",
            "supervisor"
        };

        public AuthService(SQLiteDatabase context)
        {
            _context = context;
        }

        public async Task<bool> HasAccess(string role, int? warehouseId, string resource, string method)
        {
            if (string.IsNullOrEmpty(role))
                return false;

            // Admin has full access
            if (role.ToLower() == "admin")
                return true;

            var permission = await _context.RolePermissions
                .FirstOrDefaultAsync(p => p.role == role && p.resource == resource);

            if (permission == null)
                return false;

            // Check basic permission based on HTTP method
            bool hasPermission = method.ToUpper() switch
            {
                "GET" => permission.can_view,
                "POST" => permission.can_create,
                "PUT" => permission.can_update,
                "DELETE" => permission.can_delete,
                _ => false
            };

            if (!hasPermission)
                return false;

            // Check warehouse-specific roles
            if (_warehouseSpecificRoles.Contains(role.ToLower()))
            {
                // These roles must have a warehouse ID
                if (!warehouseId.HasValue)
                    return false;

                // They can only access their own warehouse
                if (permission.warehouse_specific)
                {
                    return true; // They've already been validated to have the correct warehouseId through JWT
                }
            }

            return true;
        }
    }
}