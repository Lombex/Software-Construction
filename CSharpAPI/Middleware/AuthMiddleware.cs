using CSharpAPI.Services;
using CSharpAPI.Services.auth;


namespace CSharpAPI.Middleware
{
    public class AuthMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly IJwtService _jwtService;
        private readonly IAuthService _authService;

        public AuthMiddleware(RequestDelegate next, IJwtService jwtService, IAuthService authService)
        {
            _next = next;
            _jwtService = jwtService;
            _authService = authService;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            // Skip auth for token generation endpoint if it's an admin generating tokens
            if (context.Request.Path.StartsWithSegments("/api/v1/auth/token"))
            {
                await _next(context);
                return;
            }

            string? token = context.Request.Headers["Authorization"].FirstOrDefault()?.Split(" ").Last();

            if (token != null)
            {
                string role;
                int? warehouseId;

                if (_jwtService.ValidateToken(token, out role, out warehouseId))
                {
                    var resource = context.Request.Path.Value?.Split('/')
                        .Skip(3)  // Skip /api/v1/
                        .FirstOrDefault();

                    if (resource != null)
                    {
                        var hasAccess = await _authService.HasAccess(
                            role, 
                            warehouseId, 
                            resource, 
                            context.Request.Method
                        );

                        if (hasAccess)
                        {
                            context.Items["Role"] = role;
                            if (warehouseId.HasValue)
                            {
                                context.Items["WarehouseId"] = warehouseId.Value;
                            }

                            await _next(context);
                            return;
                        }
                    }
                }
            }

            context.Response.StatusCode = 401;
            await context.Response.WriteAsync("Unauthorized");
        }
    }

    public static class AuthMiddlewareExtensions
    {
        public static IApplicationBuilder UseAuthMiddleware(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<AuthMiddleware>();
        }
    }
}