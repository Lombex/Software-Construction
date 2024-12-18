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
            if (request == null || string.IsNullOrEmpty(request.Role))
            {
                return BadRequest("Invalid request");
            }

            // Get the API key from the Authorization header
            var authHeader = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last();
            if (string.IsNullOrEmpty(authHeader))
            {
                return Unauthorized("No authorization header provided");
            }

            // Check if it's the superadmin key
            if (authHeader != _jwtService.SuperAdminApiKey)
            {
                return Unauthorized("Invalid credentials");
            }

            // Validate requested role
            if (!IsValidRole(request.Role))
            {
                return BadRequest("Invalid role specified");
            }

            // Generate new API key and token
            string apiKey = _jwtService.CreateApiKey();
            var token = _jwtService.GenerateToken(apiKey, request.WarehouseId, request.Role);

            return Ok(new { token, apiKey });
        }

        [HttpPost("apikey")]
        public IActionResult CreateApiKey()
        {
            var authHeader = Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last();
            if (string.IsNullOrEmpty(authHeader))
            {
                return Unauthorized("No authorization header provided");
            }

            if (authHeader != _jwtService.SuperAdminApiKey)
            {
                return Unauthorized("Only superadmin can create new API keys");
            }

            var newApiKey = _jwtService.CreateApiKey();
            return Ok(new { apiKey = newApiKey });
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