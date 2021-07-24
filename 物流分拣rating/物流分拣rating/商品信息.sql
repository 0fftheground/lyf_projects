select a.OpAreaId as area_id,b.area_sku,b.skusn as sku,b.product_name,b.product_spec,b.category_id,b.category_name,
              b.parent_category_id,b.parent_category_name,
              b.vendor_code,a.DeliveryDate,b.sale_unit_qty,b.sale_stock_qty,c.stock_qty  
              from xsyx_logistics_product.tb_product_skusn_advance a,xsyx_logistics_product.tb_product_skusn b 
              LEFT JOIN xsyx_logistics_product.tb_product_storage_ref c 
              on b.storage_ref_id=c.id and c.unit_name is not null and c.is_delete=0 
              where a.OpAreaId=101 and 
              a.DeliveryDate BETWEEN '2020-11-01' and '2021-04-14' 
              and a.SkuSn=b.skusn and skusn_status<>'DELETED' ORDER BY b.area_sku
              
              
select a.OpAreaId as area_id,b.area_sku,b.skusn as sku,e.PickEmpID,e.PickEmpName, b.product_name,b.product_spec,b.category_id,b.category_name,
              b.parent_category_id,b.parent_category_name,
              b.vendor_code,a.DeliveryDate,b.sale_unit_qty,b.sale_stock_qty,c.stock_qty from             
(select DeliveryTime, PickEmpName,PickEmpID,SKU from 
xsyx_f6_picking.t_product_pick where OpAreaID = 101 and BatPickStatus = 3 and WID = 10139 and 
(DeliveryTime BETWEEN '2020-11-01 00:00:00' and '2021-04-14 23:59:59') 
and (StartPickingTime BETWEEN date_sub(DeliveryTime,interval 1 hour) and date_add(DeliveryTime,interval 11 hour))) e

INNER JOIN 
(select OpAreaId, DeliveryDate,SkuSn from xsyx_logistics_product.tb_product_skusn_advance where OpAreaId=101 and DeliveryDate BETWEEN '2020-11-01' and '2021-04-14')a on a.SkuSn=e.SKU

INNER JOIN xsyx_logistics_product.tb_product_skusn b on a.SkuSn=b.skusn and skusn_status<>'DELETED'
INNER JOIN xsyx_logistics_product.tb_product_storage_ref c  on b.storage_ref_id=c.id and c.unit_name is not null and c.is_delete=0
ORDER  BY a.DeliveryDate,e.PickEmpName;
