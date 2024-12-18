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
        private readonly SQLiteDatabase _db;

        public AuthService(SQLiteDatabase db)
        {
            _db = db;
        }

        public async Task<bool> HasAccess(string role, int? warehouseId, string resource, string method)
        {
            if (string.IsNullOrEmpty(role)) return false;
                    
            // Admin has full access regardless of warehouse
            if (role == "Admin") return true;
        
            var permission = await _db.RolePermissions
                .FirstOrDefaultAsync(p => p.role == role && p.resource == resource.ToLower());
        
            if (permission == null) return false;
        
            // If the permission is warehouse specific, we MUST have a warehouse ID in the token
            if (permission.warehouse_specific && !warehouseId.HasValue)
            {
                return false;
            }
        
            // If we're accessing a warehouse-specific resource, check if it belongs to the user's warehouse
            if (permission.warehouse_specific)
            {
                // For warehouse-specific resources, check the resource's warehouse ID against the token's warehouse ID
                switch (resource.ToLower())
                {
                    case "locations":
                        var location = await _db.Location.FirstOrDefaultAsync(l => l.id == int.Parse(resource));
                        if (location?.warehouse_id != warehouseId) return false;
                        break;
                    case "inventories":
                        var inventory = await _db.Inventors.FirstOrDefaultAsync(i => i.id == int.Parse(resource));
                        // Need to check if inventory's location is in user's warehouse
                        if (inventory != null && inventory.locations != null)
                        {
                            var locationInWarehouse = await _db.Location
                                .AnyAsync(l => inventory.locations.Contains(l.id) && l.warehouse_id == warehouseId);
                            if (!locationInWarehouse) return false;
                        }
                        break;
                    // Add other warehouse-specific resources here
                }
            }
        
            // Finally check the actual permission
            return method.ToUpper() switch
            {
                "GET" => permission.can_view,
                "POST" => permission.can_create,
                "PUT" => permission.can_update,
                "DELETE" => permission.can_delete,
                _ => false
            };
        }
    }
}