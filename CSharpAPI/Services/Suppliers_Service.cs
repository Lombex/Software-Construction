using CSharpAPI.Models;
using Newtonsoft.Json;

namespace CSharpAPI.Service {
    public class SupplierService {
        private readonly string dummydata = "data/suppliers.json";

        public List<SuppliersModel> GetAllSuppliers() {
            if (!File.Exists(dummydata)) return new List<SuppliersModel>();
            return JsonConvert.DeserializeObject<List<SuppliersModel>>(File.ReadAllText(dummydata)) ?? new List<SuppliersModel>();

            // returns dummy data
        }

        public SuppliersModel GetSupplierById(int id) {
            var _supplier = GetAllSuppliers().FirstOrDefault(x => x.id == id);
            if (_supplier == null) throw new Exception("This Supplier does not exist!");
            return _supplier;
        }

        public List<ItemsModel> GetItemFromSupplierId(int id) {
            var _supplier = GetAllSuppliers().FirstOrDefault(x => x.id == id);
            /* 
                Check if supplier id is same for item supplier id 
                if those are equal then list them up other wise return nothing
            */
            return null; // temp
        }

    }

    public interface ISupplierService {
        List<SuppliersModel> GetAllSuppliers();
        SuppliersModel GetSupplierById(int id);
        List<ItemsModel> GetItemFromSupplierId(int id);
        bool UpdateSupplier(int id, SuppliersModel supplier);
        void CreateSupplier(SuppliersModel supplier);
        bool DeleteSupplier(int id);
    }
}