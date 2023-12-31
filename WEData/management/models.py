from django.db import models





class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, db_column='CustomerID')
    name = models.CharField(max_length=255, db_column='Name')

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name





class Order(models.Model):
    sage_order_number = models.IntegerField(primary_key=True, db_column='SageOrderNumber')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='CustomerID')
    order_date = models.DateField(db_column='OrderDate')
    delivery_postcode = models.CharField(max_length=255, db_column='DeliveryPostcode')
    customer_postcode = models.CharField(max_length=255, db_column='CustomerPostcode')
    order_taken_by = models.CharField(max_length=255, db_column='OrderTakenBy')
    estimated_delivery_wkc = models.DateField(db_column='EstimatedDeliveryWkC')
    value = models.CharField(max_length=255, db_column='Value')
    order_notes = models.TextField(db_column='OrderNotes')
    status = models.CharField(max_length=50, default='Pending', db_index = True)
    user_notes = models.TextField(db_column='UserNotes', blank=True, null=True)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return str(self.sage_order_number)





class PartDescription(models.Model):
    product_code = models.CharField(max_length=255, primary_key=True, db_column='ProductCode')
    product_description = models.TextField(db_column='ProductDescription')
    weight = models.FloatField(db_column='Weight')

    class Meta:
        db_table = 'partdescription'

    def __str__(self):
        return self.product_code







class Part(models.Model):
    part_id = models.AutoField(primary_key=True, db_column='PartID')
    sage_order_number = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='SageOrderNumber')
    product_code = models.ForeignKey(PartDescription, on_delete=models.CASCADE, db_column='ProductCode')
    dept = models.CharField(max_length=255, db_column='Dept')
    machine_status = models.CharField(max_length=255, db_column='MachineStatus')
    picking_status = models.CharField(max_length=255, db_column='PickingStatus')
    assembly_status = models.CharField(max_length=255, db_column='AssemblyStatus')

    class Meta:
        db_table = 'part'

    def __str__(self):
        return str(self.part_id)








class OrdertoJobBridge(models.Model):
    bridge_id = models.AutoField(primary_key=True, db_column='BridgeID')
    job = models.CharField(max_length=255, db_column='Job')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, db_column='PartID')

    class Meta:
        db_table = 'ordertojobbridge'

    def __str__(self):
        return self.job







class CNCMachineDescription(models.Model):
    machine_id = models.CharField(max_length=255, primary_key=True, db_column='MachineID')
    machine_name = models.CharField(max_length=255, db_column='MachineName')

    class Meta:
        db_table = 'cncmachinedescription'

    def __str__(self):
        return self.machine_name





class CNCMachine(models.Model):
    cnc_machine_id = models.AutoField(primary_key=True, db_column='CNCMachineID')
    machine = models.ForeignKey(CNCMachineDescription, on_delete=models.CASCADE, db_column='MachineID')
    job = models.ForeignKey(OrdertoJobBridge, on_delete=models.CASCADE, db_column='Job')
    sheets = models.CharField(max_length=255, db_column='Sheets')
    machine_stage = models.CharField(max_length=255, db_column='MachineStage')
    date_complete = models.DateTimeField(db_column='DateComplete')
    notes = models.TextField(db_column='Notes')
    total_pieces = models.IntegerField(db_column='TotalPieces')

    class Meta:
        db_table = 'cncmachine'

    def __str__(self):
        return str(self.cnc_machine_id)





class PickingProcess(models.Model):
    picking_id = models.AutoField(primary_key=True, db_column='PickingID')
    job = models.ForeignKey(OrdertoJobBridge, on_delete=models.CASCADE, db_column='Job')
    picking_status = models.CharField(max_length=255, db_column='PickingStatus')
    date_complete = models.DateTimeField(db_column='DateComplete')
    notes = models.TextField(db_column='Notes')

    class Meta:
        db_table = 'pickingprocess'

    def __str__(self):
        return str(self.picking_id)





class WorkshopTypes(models.Model):
    workshop_id = models.AutoField(primary_key=True, db_column='WorkshopID')
    workshop_name = models.CharField(max_length=255, db_column='WorkshopName')

    class Meta:
        db_table = 'workshoptypes'

    def __str__(self):
        return self.workshop_name



class Workshop(models.Model):
    workshop_id = models.IntegerField(db_column='WorkshopID', primary_key=True)
    sage_order_number = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='SageOrderNumber')
    product_code = models.ForeignKey(PartDescription, on_delete=models.CASCADE, db_column='ProductCode')
    assembly_status = models.CharField(max_length=255, db_column='AssemblyStatus')
    notes = models.TextField(db_column='Notes')

    class Meta:
        db_table = 'workshop'

    def __str__(self):
        return f"Workshop ID: {self.workshop_id}"
