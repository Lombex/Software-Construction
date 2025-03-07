namespace CSharpAPI.Models
{
    public class ArchivedSupplierModel
    {
        public int id { get; set; }
        public string? code { get; set; }
        public string? name { get; set; }
        public string? address { get; set; }
        public string? address_extra { get; set; }
        public string? city { get; set; }
        public string? zip_code { get; set; }
        public string? province { get; set; }
        public string? country { get; set; }
        public Contact? contact { get; set; }
        public string? reference { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public DateTime archived_at { get; set; }
    }
}
