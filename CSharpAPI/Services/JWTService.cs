using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace CSharpAPI.Services
{
    public interface IJwtService
    {
        string GenerateToken(string role, int? warehouseId);
        bool ValidateToken(string token, out string role, out int? warehouseId);
    }

    public class JwtService : IJwtService
    {
        private readonly string _secretKey;
        private readonly string _issuer;
        private readonly string _audience;

        public JwtService(IConfiguration configuration)
        {
            _secretKey = configuration["Jwt:SecretKey"] ?? throw new ArgumentNullException("JWT Secret Key is not configured");
            _issuer = configuration["Jwt:Issuer"] ?? throw new ArgumentNullException("JWT Issuer is not configured");
            _audience = configuration["Jwt:Audience"] ?? throw new ArgumentNullException("JWT Audience is not configured");
        }

        public string GenerateToken(string role, int? warehouseId)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secretKey));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.Role, role),
            };

            if (warehouseId.HasValue)
            {
                claims.Add(new Claim("WarehouseId", warehouseId.Value.ToString()));
            }

            var token = new JwtSecurityToken(
                issuer: _issuer,
                audience: _audience,
                claims: claims,
                expires: DateTime.Now.AddYears(1), // Tokens valid for 1 year since they're distributed manually
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
                var key = Encoding.UTF8.GetBytes(_secretKey);

                tokenHandler.ValidateToken(token, new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(key),
                    ValidateIssuer = true,
                    ValidIssuer = _issuer,
                    ValidateAudience = true,
                    ValidAudience = _audience,
                    ValidateLifetime = true,
                    ClockSkew = TimeSpan.Zero
                }, out SecurityToken validatedToken);

                var jwtToken = (JwtSecurityToken)validatedToken;
                
                role = jwtToken.Claims.First(x => x.Type == ClaimTypes.Role).Value;
                
                var warehouseIdClaim = jwtToken.Claims.FirstOrDefault(x => x.Type == "WarehouseId");
                if (warehouseIdClaim != null && int.TryParse(warehouseIdClaim.Value, out int wId))
                {
                    warehouseId = wId;
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