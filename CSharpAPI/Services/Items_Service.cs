using System.Collections.Generic;
using System.IO;
using System.Linq;
using CSharpAPI.Models;
using Newtonsoft.Json;

namespace CSharpAPI.Service
{
    public class ItemsService : IItemsService
    {
        private readonly string dummydata = "data/item.json";

        public List<ItemsModel> GetAllItems()
        {
            if (!File.Exists(dummydata)) return new List<ItemsModel>();
            return JsonConvert.DeserializeObject<List<ItemsModel>>(File.ReadAllText(dummydata)) ?? new List<ItemsModel>();
        }

        public ItemsModel GetItemByUid(string uid)
        {
            var items = GetAllItems();
            return items.FirstOrDefault(item => item.uid == uid);
        }

        public bool UpdateItem(string uid, ItemsModel updateModel)
        {
            var items = GetAllItems();
            var index = items.FindIndex(item => item.uid == uid);
            if (index == -1)
            {
                return false;
            }

            items[index] = updateModel;

            File.WriteAllText(dummydata, JsonConvert.SerializeObject(items));
            return true;
        }

        public void CreateItem(ItemsModel model)
        {
            var items = GetAllItems();
            items.Add(model);

            File.WriteAllText(dummydata, JsonConvert.SerializeObject(items));
        }

        public bool DeleteItem(string uid)
        {
            var items = GetAllItems();
            var itemToRemove = items.FirstOrDefault(item => item.uid == uid);
            if (itemToRemove == null)
            {
                return false;
            }

            items.Remove(itemToRemove);

            File.WriteAllText(dummydata, JsonConvert.SerializeObject(items));
            return true;
        }
    }

    public interface IItemsService
    {
        List<ItemsModel> GetAllItems();
        ItemsModel GetItemByUid(string uid);
        bool UpdateItem(string uid, ItemsModel updateModel);
        void CreateItem(ItemsModel model);
        bool DeleteItem(string uid);
    }
}
