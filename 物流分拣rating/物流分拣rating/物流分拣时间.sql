SELECT e.DeliveryTime, e.PickEmpName,sumPickQty, sum_resttime, worktime, (worktime-sum_resttime) as actual_worktime from 

(SELECT c.DeliveryTime, c.PickEmpName, SUM(resttime) AS sum_resttime from 
(SELECT b.DeliveryTime, b.PickEmpName, resttime, n from
(SELECT a.DeliveryTime, a.PickEmpName,TIMESTAMPDIFF(SECOND , shiftendpickingtime,StartPickingTime) as resttime,
row_number() over(partition by a.DeliveryTime, a.PickEmpName order by TIMESTAMPDIFF(SECOND , shiftendpickingtime,StartPickingTime) desc) as n
from 
(select DeliveryTime, PickEmpName,StartPickingTime ,EndPickingTime,
LAG(EndPickingTime,1,0) OVER (PARTITION BY DeliveryTime, PickEmpName ORDER BY StartPickingTime ) AS shiftendpickingtime
from xsyx_f6_picking.t_product_pick where OpAreaID = 101 and BatPickStatus = 3 and WID = 10139 and 
(DeliveryTime BETWEEN '2020-11-01 00:00:00' and '2021-04-14 23:59:59') 
and (StartPickingTime BETWEEN date_sub(DeliveryTime,interval 1 hour) and date_add(DeliveryTime,interval 11 hour)) ORDER BY DeliveryTime, PickEmpName,StartPickingTime) a) b
WHERE n<=2
GROUP BY  b.DeliveryTime, b.PickEmpName) c GROUP BY c.DeliveryTime, c.PickEmpName) e

INNER JOIN 
(select DeliveryTime, PickEmpName,sum(PickQty) as sumPickQty, TIMESTAMPDIFF(SECOND , MIN(StartPickingTime),MAX(EndPickingTime)) AS worktime
from xsyx_f6_picking.t_product_pick where OpAreaID = 101 and BatPickStatus = 3 and WID = 10139 and (DeliveryTime BETWEEN '2020-11-01 00:00:00' and '2021-04-14 23:59:59') 
and (StartPickingTime BETWEEN date_sub(DeliveryTime,interval 1 hour) and date_add(DeliveryTime,interval 11 hour))
group BY DeliveryTime,PickEmpName) d 
on e.DeliveryTime = d.DeliveryTime and e.PickEmpName=d.PickEmpName 
Order by e.PickEmpName,  e.DeliveryTime;