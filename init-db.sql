-- Use the shop_db database
USE shop_db;

-- Create the Customer table
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    ContactInformation VARCHAR(255)
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
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- Create the PartDescription table
CREATE TABLE PartDescription (
    ProductCode VARCHAR(255) PRIMARY KEY,
    ProductDescription TEXT,
    Weight FLOAT
);

-- Create the Part table
CREATE TABLE Part (
    PartID INT AUTO_INCREMENT PRIMARY KEY,
    SageOrderNumber INT,
    ProductCode VARCHAR(255),
    Dept VARCHAR(255),
    MachineStatus VARCHAR(255),
    PickingStatus VARCHAR(255),
    AssemblyStatus VARCHAR(255),
    FOREIGN KEY (SageOrderNumber) REFERENCES `Order`(SageOrderNumber),
    FOREIGN KEY (ProductCode) REFERENCES PartDescription(ProductCode)
);

-- Create the CNC Machine table
CREATE TABLE CNCMachine (
    CNCMachineID INT AUTO_INCREMENT PRIMARY KEY,
    MachineID VARCHAR(255),
    Job VARCHAR(255),
    Sheets VARCHAR(255),
    MachineStage VARCHAR(255),
    DateComplete DATETIME,
    Notes TEXT,
    TotalPieces INT,
    INDEX (Job) -- Creating an index for the Job column
);

-- Create the OrdertoJobBridge table
CREATE TABLE OrdertoJobBridge (
    BridgeID INT AUTO_INCREMENT PRIMARY KEY,
    Job VARCHAR(255),
    PartID INT,
    FOREIGN KEY (Job) REFERENCES CNCMachine(Job),
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
);

-- Create the Picking Process table
CREATE TABLE PickingProcess (
    PickingID INT AUTO_INCREMENT PRIMARY KEY,
    Job VARCHAR(255),
    PickingStatus VARCHAR(255),
    DateComplete DATETIME,
    Notes TEXT,
    FOREIGN KEY (Job) REFERENCES OrdertoJobBridge(Job)
);

-- Create the WorkshopTypes table
CREATE TABLE WorkshopTypes (
    WorkshopID INT AUTO_INCREMENT PRIMARY KEY,
    WorkshopName VARCHAR(255)
);

-- Create the Workshop table
CREATE TABLE Workshop (
    WorkshopID INT,
    PartID INT,
    AssemblyStatus VARCHAR(255),
    Notes TEXT,
    FOREIGN KEY (PartID) REFERENCES Part(PartID),
    FOREIGN KEY (WorkshopID) REFERENCES WorkshopTypes(WorkshopID)
);
