using Microsoft.AspNetCore.Mvc;
using CSharpAPI.Services;

namespace CSharpAPI.Controllers
{
    [ApiController]
    [Route("api/v1/auth")]
    public class AuthController : ControllerBase
    {
        private readonly IJwtService _jwtService;

        public AuthController(IJwtService jwtService)
        {
            _jwtService = jwtService;
        }

        [HttpPost("token")]
        public IActionResult GenerateToken([FromBody] TokenRequest request)
        {
            // Check if the requesting user is admin (you might want to add additional security here)
            var authHeader = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last();
            if (authHeader == null)
            {
                return Unauthorized();
            }

            string role;
            int? warehouseId;
            if (!_jwtService.ValidateToken(authHeader, out role, out warehouseId) || role != "Admin")
            {
                return Unauthorized();
            }

            // Validate requested role
            if (!IsValidRole(request.Role))
            {
                return BadRequest("Invalid role specified");
            }

            var token = _jwtService.GenerateToken(request.Role, request.WarehouseId);
            return Ok(new { token });
        }

        private bool IsValidRole(string role)
        {
            return role switch
            {
                "Admin" or 
                "WarehouseManager" or 
                "InventoryManager" or 
                "FloorManager" or 
                "Operative" or 
                "Supervisor" or 
                "Analyst" or 
                "Logistics" or 
                "Sales" => true,
                _ => false
            };
        }
    }

    public class TokenRequest
    {
        public string Role { get; set; }
        public int? WarehouseId { get; set; }
    }
}