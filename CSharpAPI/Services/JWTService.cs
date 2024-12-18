using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace CSharpAPI.Services
{
    public interface IJwtService
    {
        string GenerateToken(string apiKey, int? warehouseId, string role);
        bool ValidateToken(string token, out string role, out int? warehouseId);
    }

    public class JwtService : IJwtService
    {
        private readonly string _secretKey;
        private readonly string _issuer;
        private readonly string _audience;

        public JwtService(IConfiguration configuration)
        {
            _secretKey = configuration["Jwt:Key"] ?? "your-256-bit-secret";
            _issuer = configuration["Jwt:Issuer"] ?? "your-issuer";
            _audience = configuration["Jwt:Audience"] ?? "your-audience";
        }

        public string GenerateToken(string apiKey, int? warehouseId, string role)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secretKey));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, apiKey),
                new Claim(ClaimTypes.Role, role)
            };

            if (warehouseId.HasValue)
            {
                claims.Add(new Claim("WarehouseId", warehouseId.Value.ToString()));
            }

            var token = new JwtSecurityToken(
                issuer: _issuer,
                audience: _audience,
                claims: claims,
                expires: DateTime.UtcNow.AddHours(1),
                signingCredentials: credentials
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public bool ValidateToken(string token, out string role, out int? warehouseId)
        {
            role = null;
            warehouseId = null;

            try
            {
                var tokenHandler = new JwtSecurityTokenHandler();
                var key = Encoding.ASCII.GetBytes(_secretKey);

                var validationParameters = new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(key),
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidIssuer = _issuer,
                    ValidAudience = _audience,
                    ClockSkew = TimeSpan.Zero
                };

                ClaimsPrincipal principal = tokenHandler.ValidateToken(token, validationParameters, out SecurityToken validatedToken);

                // Extract role
                var roleClaim = principal.FindFirst(ClaimTypes.Role);
                if (roleClaim == null)
                    return false;

                role = roleClaim.Value;

                // Extract warehouse ID if present
                var warehouseIdClaim = principal.FindFirst("WarehouseId");
                if (warehouseIdClaim != null && int.TryParse(warehouseIdClaim.Value, out int whId))
                {
                    warehouseId = whId;
                }

                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}