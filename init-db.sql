-- Use the shop_db database
USE shop_db;

-- Create the Customer table
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    ContactInformation VARCHAR(255)
);

-- Create the Order table
CREATE TABLE `Order` (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    OrderDate DATE,
    CustomerID INT,
    CustomerOrderNumber VARCHAR(255),
    DeliveryAddress VARCHAR(255),
    SalesOrderAddress VARCHAR(255),
    OrderTakenBy VARCHAR(255),
    DispatchByDate DATE,
    TotalWeight FLOAT,
    Status VARCHAR(255),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- Create the Part table
CREATE TABLE Part (
    PartID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductCode VARCHAR(255),
    Description VARCHAR(255),
    DepartmentAssigned VARCHAR(255),
    UnitPrice FLOAT,
    Weight FLOAT,
    Status VARCHAR(255),
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
);

-- Create the CNC Machine table
CREATE TABLE CNCMachine (
    MachineID INT AUTO_INCREMENT PRIMARY KEY,
    PartID INT,
    Status VARCHAR(255),
    DateComplete DATE,
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
);

-- Create the Picking Process table
CREATE TABLE PickingProcess (
    PickingID INT AUTO_INCREMENT PRIMARY KEY,
    PartID INT,
    Status VARCHAR(255),
    DateComplete DATE,
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
);

-- Create the Workshop table
CREATE TABLE Workshop (
    WorkshopID INT AUTO_INCREMENT PRIMARY KEY,
    PartID INT,
    Type VARCHAR(255),
    AssemblyStatus VARCHAR(255),
    DateComplete DATE,
    Notes VARCHAR(255),
    FOREIGN KEY (PartID) REFERENCES Part(PartID)
);
