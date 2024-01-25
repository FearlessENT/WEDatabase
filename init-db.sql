USE shop_db;

-- Create the Customer table
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255)
);

-- Create the Order table with a reference to Customer
CREATE TABLE `Order` (
    SageOrderNumber INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    DeliveryPostcode VARCHAR(255),
    CustomerPostcode VARCHAR(255),
    OrderTakenBy VARCHAR(255),
    EstimatedDeliveryWkC DATE,
    Value VARCHAR(255),
    OrderNotes TEXT,
    Status VARCHAR(50) DEFAULT 'Pending',
    UserNotes TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- Create the PartDescription table
CREATE TABLE PartDescription (
    ProductCode VARCHAR(255) PRIMARY KEY,
    ProductDescription TEXT,
    Weight FLOAT
);

-- Create the Job table
CREATE TABLE Job (
    JOBID INT AUTO_INCREMENT PRIMARY KEY,
    JobName VARCHAR(255) UNIQUE,
    CNCMachineID VARCHAR(255),
    mm8_notes TEXT,
    mm8_quantity TEXT,
    mm8_status TEXT,  -- New mm8_status column
    mm18_notes TEXT,
    mm18_quantity TEXT,
    mm18_status TEXT,  -- New mm18_status column
    FOREIGN KEY (CNCMachineID) REFERENCES CNCMachineDescription(MachineID)
);

-- Modify the Part table to include a foreign key to Job
CREATE TABLE Part (
    PartID INT AUTO_INCREMENT PRIMARY KEY,
    SageOrderNumber INT,
    ProductCode VARCHAR(255),
    Dept VARCHAR(255),
    MachineStatus VARCHAR(255),
    PickingStatus VARCHAR(255),
    AssemblyStatus VARCHAR(255),
    JOBID INT,
    FOREIGN KEY (SageOrderNumber) REFERENCES `Order`(SageOrderNumber),
    FOREIGN KEY (ProductCode) REFERENCES PartDescription(ProductCode),
    FOREIGN KEY (JOBID) REFERENCES Job(JOBID)
);

-- Create the CNCMachineDescription table
CREATE TABLE CNCMachineDescription (
    MachineID VARCHAR(255) PRIMARY KEY,
    MachineName VARCHAR(255)
);

-- Modify the CNCMachine table to include a JobID column
CREATE TABLE CNCMachine (
    CNCMachineID INT AUTO_INCREMENT PRIMARY KEY,
    MachineID VARCHAR(255),
    JobID INT,
    Sheets VARCHAR(255),
    MachineStage VARCHAR(255),
    DateComplete DATETIME,
    Notes TEXT,
    TotalPieces INT,
    FOREIGN KEY (MachineID) REFERENCES CNCMachineDescription(MachineID),
    FOREIGN KEY (JobID) REFERENCES Job(JOBID)
);

-- Modify the Picking Process table to include a JobID column
CREATE TABLE PickingProcess (
    PickingID INT AUTO_INCREMENT PRIMARY KEY,
    JobID INT,
    PickingStatus VARCHAR(255),
    DateComplete DATETIME,
    Notes TEXT,
    FOREIGN KEY (JobID) REFERENCES Job(JOBID)
);

-- Create the WorkshopTypes table
CREATE TABLE WorkshopTypes (
    WorkshopID INT AUTO_INCREMENT PRIMARY KEY,
    WorkshopName VARCHAR(255)
);

-- Create the Workshop table
CREATE TABLE Workshop (
    WorkshopID INT,
    SageOrderNumber INT,
    ProductCode VARCHAR(255),
    AssemblyStatus VARCHAR(255),
    Notes TEXT,
    FOREIGN KEY (WorkshopID) REFERENCES WorkshopTypes(WorkshopID),
    FOREIGN KEY (SageOrderNumber) REFERENCES `Order`(SageOrderNumber),
    FOREIGN KEY (ProductCode) REFERENCES PartDescription(ProductCode)
);



-- Create Profile table linking auth_user to CNCMachineDescription
CREATE TABLE Profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    cnc_machine_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (cnc_machine_id) REFERENCES CNCMachineDescription(MachineID)
);
