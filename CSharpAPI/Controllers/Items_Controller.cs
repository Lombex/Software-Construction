using CSharpAPI.Models;
using CSharpAPI.Service;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace CSharpAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ItemController : ControllerBase
    {
        private readonly IItemsService _itemService;

        public ItemController(IItemsService itemService)
        {
            _itemService = itemService;
        }

        [HttpGet]
        public ActionResult<List<ItemsModel>> GetAllItems()
        {
            return Ok(_itemService.GetAllItems());
        }

        [HttpGet("{uid}")]
        public ActionResult<ItemsModel> GetItemByUid(string uid)
        {
            var item = _itemService.GetItemByUid(uid);
            if (item == null)
            {
                return NotFound();
            }
            return Ok(item);
        }

        [HttpPost]
        public ActionResult CreateItem([FromBody] ItemsModel item)
        {
            if (item == null)
            {
                return BadRequest();
            }

            _itemService.CreateItem(item);
            return CreatedAtAction(nameof(GetItemByUid), new { uid = item.uid }, item);
        }

        [HttpPut("{uid}")]
        public ActionResult UpdateItem(string uid, [FromBody] ItemsModel updateItem)
        {
            if (!_itemService.UpdateItem(uid, updateItem))
            {
                return NotFound();
            }
            return NoContent();
        }

        [HttpDelete("{uid}")]
        public ActionResult DeleteItem(string uid)
        {
            if (!_itemService.DeleteItem(uid))
            {
                return NotFound();
            }
            return NoContent();
        }
    }
}
