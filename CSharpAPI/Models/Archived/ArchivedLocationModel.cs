namespace CSharpAPI.Models
{
    public class ArchivedLocationModel
    {
        public int id { get; set; }
        public int warehouse_id { get; set; }
        public string? code { get; set; }
        public string? name { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public DateTime archived_at { get; set; }
    }
}
