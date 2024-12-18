using CSharpAPI.Services;

namespace CSharpAPI.Middleware
{
    public class AuthMiddleware
    {
        private readonly RequestDelegate _next;

        public AuthMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context, IJwtService jwtService, IAuthService authService)
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

                if (jwtService.ValidateToken(token, out role, out warehouseId))
                {
                    var resource = context.Request.Path.Value?.Split('/')
                        .Skip(3)  // Skip /api/v1/
                        .FirstOrDefault();

                    if (resource != null)
                    {
                        var hasAccess = await authService.HasAccess(
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