﻿// <auto-generated />
using System;
using CSharpAPI.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace CSharpAPI.Migrations
{
    [DbContext(typeof(SQLiteDatabase))]
    [Migration("20241211093732_AddRolePermissions")]
    partial class AddRolePermissions
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder.HasAnnotation("ProductVersion", "9.0.0");

            modelBuilder.Entity("CSharpAPI.Models.Auth.ApiUser", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("api_key")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("app")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("role")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.Property<int?>("warehouse_id")
                        .HasColumnType("INTEGER");

                    b.HasKey("id");

                    b.HasIndex("api_key")
                        .IsUnique();

                    b.ToTable("ApiUsers");
                });

            modelBuilder.Entity("CSharpAPI.Models.Auth.RolePermission", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<bool>("can_create")
                        .HasColumnType("INTEGER");

                    b.Property<bool>("can_delete")
                        .HasColumnType("INTEGER");

                    b.Property<bool>("can_update")
                        .HasColumnType("INTEGER");

                    b.Property<bool>("can_view")
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("resource")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("role")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.HasIndex("role", "resource")
                        .IsUnique();

                    b.ToTable("RolePermissions");
                });

            modelBuilder.Entity("CSharpAPI.Models.ClientModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("address")
                        .HasColumnType("TEXT");

                    b.Property<string>("city")
                        .HasColumnType("TEXT");

                    b.Property<string>("contact_email")
                        .HasColumnType("TEXT");

                    b.Property<string>("contact_name")
                        .HasColumnType("TEXT");

                    b.Property<string>("contact_phone")
                        .HasColumnType("TEXT");

                    b.Property<string>("country")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<string>("province")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("zip_code")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("ClientModels");
                });

            modelBuilder.Entity("CSharpAPI.Models.InventorieModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("description")
                        .HasColumnType("TEXT");

                    b.Property<string>("item_id")
                        .HasColumnType("TEXT");

                    b.Property<string>("item_reference")
                        .HasColumnType("TEXT");

                    b.PrimitiveCollection<string>("locations")
                        .HasColumnType("TEXT");

                    b.Property<int>("total_allocated")
                        .HasColumnType("INTEGER");

                    b.Property<int>("total_available")
                        .HasColumnType("INTEGER");

                    b.Property<int>("total_expected")
                        .HasColumnType("INTEGER");

                    b.Property<int>("total_on_hand")
                        .HasColumnType("INTEGER");

                    b.Property<int>("total_ordered")
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("Inventors");
                });

            modelBuilder.Entity("CSharpAPI.Models.ItemGroupModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("description")
                        .HasColumnType("TEXT");

                    b.Property<int>("itemtype_id")
                        .HasColumnType("INTEGER");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("ItemGroups");
                });

            modelBuilder.Entity("CSharpAPI.Models.ItemLineModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("description")
                        .HasColumnType("TEXT");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("ItemLine");
                });

            modelBuilder.Entity("CSharpAPI.Models.ItemModel", b =>
                {
                    b.Property<string>("uid")
                        .HasColumnType("TEXT");

                    b.Property<string>("code")
                        .HasColumnType("TEXT");

                    b.Property<string>("commodity_code")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("description")
                        .HasColumnType("TEXT");

                    b.Property<int>("item_group")
                        .HasColumnType("INTEGER");

                    b.Property<int>("item_line")
                        .HasColumnType("INTEGER");

                    b.Property<int>("item_type")
                        .HasColumnType("INTEGER");

                    b.Property<string>("model_number")
                        .HasColumnType("TEXT");

                    b.Property<int>("pack_order_quantity")
                        .HasColumnType("INTEGER");

                    b.Property<string>("short_description")
                        .HasColumnType("TEXT");

                    b.Property<string>("supplier_code")
                        .HasColumnType("TEXT");

                    b.Property<int>("supplier_id")
                        .HasColumnType("INTEGER");

                    b.Property<string>("supplier_part_number")
                        .HasColumnType("TEXT");

                    b.Property<int>("unit_order_quantity")
                        .HasColumnType("INTEGER");

                    b.Property<int>("unit_purchase_quantity")
                        .HasColumnType("INTEGER");

                    b.Property<string>("upc_code")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("uid");

                    b.ToTable("itemModels");
                });

            modelBuilder.Entity("CSharpAPI.Models.ItemTypeModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("description")
                        .HasColumnType("TEXT");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("ItemType");
                });

            modelBuilder.Entity("CSharpAPI.Models.Items", b =>
                {
                    b.Property<string>("item_id")
                        .HasColumnType("TEXT");

                    b.Property<int>("amount")
                        .HasColumnType("INTEGER");

                    b.HasKey("item_id");

                    b.ToTable("Items");
                });

            modelBuilder.Entity("CSharpAPI.Models.LocationModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("code")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.Property<int>("warehouse_id")
                        .HasColumnType("INTEGER");

                    b.HasKey("id");

                    b.ToTable("Location");
                });

            modelBuilder.Entity("CSharpAPI.Models.OrderModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<int>("bill_to")
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("items")
                        .HasColumnType("TEXT");

                    b.Property<string>("notes")
                        .HasColumnType("TEXT");

                    b.Property<string>("order_date")
                        .HasColumnType("TEXT");

                    b.Property<string>("order_status")
                        .HasColumnType("TEXT");

                    b.Property<string>("picking_notes")
                        .HasColumnType("TEXT");

                    b.Property<string>("reference")
                        .HasColumnType("TEXT");

                    b.Property<string>("reference_extra")
                        .HasColumnType("TEXT");

                    b.Property<string>("request_date")
                        .HasColumnType("TEXT");

                    b.Property<int>("ship_to")
                        .HasColumnType("INTEGER");

                    b.Property<int>("shipment_id")
                        .HasColumnType("INTEGER");

                    b.Property<string>("shipping_notes")
                        .HasColumnType("TEXT");

                    b.Property<int>("source_id")
                        .HasColumnType("INTEGER");

                    b.Property<float>("total_amount")
                        .HasColumnType("REAL");

                    b.Property<float>("total_discount")
                        .HasColumnType("REAL");

                    b.Property<float>("total_surcharge")
                        .HasColumnType("REAL");

                    b.Property<float>("total_tax")
                        .HasColumnType("REAL");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.Property<int>("warehouse_id")
                        .HasColumnType("INTEGER");

                    b.HasKey("id");

                    b.ToTable("Order");
                });

            modelBuilder.Entity("CSharpAPI.Models.ShipmentModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("carrier_code")
                        .HasColumnType("TEXT");

                    b.Property<string>("carrier_description")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("items")
                        .HasColumnType("TEXT");

                    b.Property<string>("notes")
                        .HasColumnType("TEXT");

                    b.Property<string>("order_date")
                        .HasColumnType("TEXT");

                    b.Property<int>("order_id")
                        .HasColumnType("INTEGER");

                    b.Property<string>("payment_type")
                        .HasColumnType("TEXT");

                    b.Property<string>("request_date")
                        .HasColumnType("TEXT");

                    b.Property<string>("service_code")
                        .HasColumnType("TEXT");

                    b.Property<string>("shipment_date")
                        .HasColumnType("TEXT");

                    b.Property<string>("shipment_status")
                        .HasColumnType("TEXT");

                    b.Property<string>("shipment_type")
                        .HasColumnType("TEXT");

                    b.Property<int>("source_id")
                        .HasColumnType("INTEGER");

                    b.Property<int>("total_package_count")
                        .HasColumnType("INTEGER");

                    b.Property<float>("total_package_weight")
                        .HasColumnType("REAL");

                    b.Property<string>("transfer_mode")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("Shipment");
                });

            modelBuilder.Entity("CSharpAPI.Models.SupplierModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("address")
                        .HasColumnType("TEXT");

                    b.Property<string>("address_extra")
                        .HasColumnType("TEXT");

                    b.Property<string>("city")
                        .HasColumnType("TEXT");

                    b.Property<string>("code")
                        .HasColumnType("TEXT");

                    b.Property<string>("contact_name")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<string>("phonenumber")
                        .HasColumnType("TEXT");

                    b.Property<string>("province")
                        .HasColumnType("TEXT");

                    b.Property<string>("reference")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("zip_code")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("Suppliers");
                });

            modelBuilder.Entity("CSharpAPI.Models.TransferModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("items")
                        .HasColumnType("TEXT");

                    b.Property<string>("reference")
                        .HasColumnType("TEXT");

                    b.Property<int?>("transfer_from")
                        .HasColumnType("INTEGER");

                    b.Property<string>("transfer_status")
                        .HasColumnType("TEXT");

                    b.Property<int>("transfer_to")
                        .HasColumnType("INTEGER");

                    b.Property<DateTime?>("updated_at")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("Transfer");
                });

            modelBuilder.Entity("CSharpAPI.Models.WarehouseModel", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("address")
                        .HasColumnType("TEXT");

                    b.Property<string>("city")
                        .HasColumnType("TEXT");

                    b.Property<string>("code")
                        .HasColumnType("TEXT");

                    b.Property<string>("country")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("created_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("name")
                        .HasColumnType("TEXT");

                    b.Property<string>("province")
                        .HasColumnType("TEXT");

                    b.Property<DateTime>("updated_at")
                        .HasColumnType("TEXT");

                    b.Property<string>("zip")
                        .HasColumnType("TEXT");

                    b.HasKey("id");

                    b.ToTable("Warehouse");
                });

            modelBuilder.Entity("CSharpAPI.Models.WarehouseModel", b =>
                {
                    b.OwnsOne("CSharpAPI.Models.Contact", "contact", b1 =>
                        {
                            b1.Property<int>("WarehouseModelid")
                                .HasColumnType("INTEGER");

                            b1.Property<string>("email")
                                .HasColumnType("TEXT");

                            b1.Property<string>("name")
                                .HasColumnType("TEXT");

                            b1.Property<string>("phone")
                                .HasColumnType("TEXT");

                            b1.HasKey("WarehouseModelid");

                            b1.ToTable("contacts");

                            b1.WithOwner()
                                .HasForeignKey("WarehouseModelid");
                        });

                    b.Navigation("contact");
                });
#pragma warning restore 612, 618
        }
    }
}