from django.db import models





class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, db_column='CustomerID')
    name = models.CharField(max_length=255, db_column='Name')

    class Meta:
        db_table = 'Customer'

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
        db_table = 'PartDescription'

    def __str__(self):
        return self.product_code







class CNCMachineDescription(models.Model):
    machine_id = models.CharField(max_length=255, primary_key=True, db_column='MachineID')
    machine_name = models.CharField(max_length=255, db_column='MachineName')

    class Meta:
        db_table = 'CNCMachineDescription'

    def __str__(self):
        return self.machine_name



from django.conf import settings

class Job(models.Model):
    job_id = models.AutoField(primary_key=True, db_column='JOBID')
    job_name = models.CharField(max_length=255, unique=True, db_column='JobName')
    job_notes = models.TextField(db_column = 'JobNotes')

    mm8_notes = models.TextField(db_column='mm8_notes', blank=True, null=True)
    mm8_quantity = models.TextField(db_column='mm8_quantity', blank=True, null=True)
    mm18_notes = models.TextField(db_column='mm18_notes', blank=True, null=True)
    mm18_quantity = models.TextField(db_column='mm18_quantity', blank=True, null=True)

    machined_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='machined_jobs')

    CNCMachine = models.ForeignKey(
        CNCMachineDescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='CNCMachineID' 
    )

    mm8_status = models.TextField(db_column='mm8_status', blank=True, null=True)
    mm18_status = models.TextField(db_column='mm18_status', blank=True, null=True)


    class Meta:
        db_table = 'Job'

    def __str__(self):
        return self.job_name




class Part(models.Model):
    part_id = models.AutoField(primary_key=True, db_column='PartID')
    sage_order_number = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='SageOrderNumber')
    product_code = models.ForeignKey(PartDescription, on_delete=models.CASCADE, db_column='ProductCode')
    dept = models.CharField(max_length=255, db_column='Dept')
    machine_status = models.CharField(max_length=255, db_column='MachineStatus')
    picking_status = models.CharField(max_length=255, db_column='PickingStatus')
    assembly_status = models.CharField(max_length=255, db_column='AssemblyStatus')
    sage_comment1 = models.TextField(db_column='SageComment1', blank=True, null=True)  # Added field
    sage_comment2 = models.TextField(db_column='SageComment2', blank=True, null=True)  # Added field
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_column='JOBID')

    class Meta:
        db_table = 'Part'

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








class CNCMachine(models.Model):
    cnc_machine_id = models.AutoField(primary_key=True, db_column='CNCMachineID')
    machine = models.ForeignKey(CNCMachineDescription, on_delete=models.CASCADE, db_column='MachineID')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_column='JobID')  # Updated to reference Job model
    sheets = models.CharField(max_length=255, db_column='Sheets')
    machine_stage = models.CharField(max_length=255, db_column='MachineStage')
    date_complete = models.DateTimeField(db_column='DateComplete')
    notes = models.TextField(db_column='Notes')
    total_pieces = models.IntegerField(db_column='TotalPieces')

    class Meta:
        db_table = 'CNCMachine'

    def __str__(self):
        return str(self.cnc_machine_id)




class PickingProcess(models.Model):
    picking_id = models.AutoField(primary_key=True, db_column='PickingID')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_column='JobID')  # Updated to reference Job model
    picking_status = models.CharField(max_length=255, db_column='PickingStatus')
    date_complete = models.DateTimeField(db_column='DateComplete')
    notes = models.TextField(db_column='Notes')

    class Meta:
        db_table = 'PickingProcess'

    def __str__(self):
        return str(self.picking_id)



class WorkshopTypes(models.Model):
    workshop_id = models.AutoField(primary_key=True, db_column='WorkshopID')
    workshop_name = models.CharField(max_length=255, db_column='WorkshopName')

    class Meta:
        db_table = 'WorkshopTypes'

    def __str__(self):
        return self.workshop_name




class Workshop(models.Model):
    id = models.AutoField(primary_key=True)
    workshop_id = models.ForeignKey(WorkshopTypes, on_delete=models.CASCADE, db_column='WorkshopID')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, db_column='PartID', related_name='workshops')  # New link to Part
    assembly_status = models.CharField(max_length=255, db_column='AssemblyStatus')
    notes = models.TextField(db_column='Notes')

    class Meta:
        db_table = 'Workshop'

    def __str__(self):
        return f"Workshop ID: {self.workshop_id.workshop_name}, Part ID: {self.part.part_id}"







class MiscTable(models.Model):
    part = models.OneToOneField(Part, on_delete=models.CASCADE, primary_key=True, db_column='PartID')
    date_added = models.DateTimeField(auto_now_add=True, db_column = 'date_added')

    class Meta:
        db_table = 'MiscTable'
        ordering = ['-date_added']

    def __str__(self):
        return f"Miscellaneous Part ID: {self.part.part_id}"
    





class Upholstery(models.Model):
    upholstery_id = models.AutoField(primary_key=True, db_column='UpholsteryID')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, db_column='PartID', related_name='upholsteries')
    comments = models.TextField(db_column='Comments', blank=True, null=True)
    comment2 = models.TextField(db_column='Comment2', blank=True, null=True)  # Added field
    value = models.CharField(max_length=255, db_column='Value', blank=True, null=True)
    pre_booked_date = models.DateField(db_column='PreBookedDate', blank=True, null=True)
    routed_date = models.DateField(db_column='RoutedDate', blank=True, null=True)
    assembly_status = models.CharField(max_length=255, db_column='AssemblyStatus', blank=True, null=True)
    assembly_notes = models.TextField(db_column='AssemblyNotes', blank=True, null=True)

    class Meta:
        db_table = 'Upholstery'

    def __str__(self):
        return f"Upholstery ID: {self.upholstery_id}"