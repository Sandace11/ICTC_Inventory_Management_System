# Models

This file contains all the information about the models involved in this project. A short description of each model and the 
relationship between them is given below.

## Category

It is the category of the product / type involved. It is the most general level of categorization. Some common values of category can be:
- Electronics
- Furniture
- Utilities
  
The required fields involved in category are:
- `categoryName`: Name of the category

## Type

Type indicates the type of a product. Some examples of type are:
- Computer
- Printers
- UPS
- Notice Board
- Chair
- Table

The required fields of this category are:
- `typeName`: Name of th etype
- `category`: The category of the type


## Product

It is the actual product in the inventory. Some examples are:

- HP Laserjet 400
- Samsung Smart TV
- Notice Board

In some cases, like Notice Board, create a category called Furniture. Also, create a type Notice Board and add item called Notice Board. It will make it easier to search item in the future.

The required fields of a product are:
- `type`: The type of the product.
- `name`: Name of the product.
- `room`: The room in which the product is kept.
- `working`: The number of working items of this product
- `inMaintenance`: Number of items in maintenance
- `damaged`: Number of damaged products

The optional fields are:
- `unitCost`: Cost of 1 unit
- `donor`: Donor (null if purchased)
- `properties`: Custom attributes of the product, eg. SSD size, etc. You can add this for yourself.
- `remarks`: Remarks

The fields which are automatically added and udpated are:
- `firstAddedDate`
- `lastModifiedDate`

If the item is purchased, leave donor empty.

## SubProduct

Some product have sub products within them. For example your PC may have more than one part. These are subproducts. If your PC is a product, then its monitors, keyboards, mice and speakers can be modelled as subproduct.

The required fields are:
- `product`
- `name`
- `working`
- `inMaintenance`
- `damaged`

The optional fields are:
- `unitCost`
- `properties`
- `remarks`

The automatically added and modified fields are:

- `firstAddedDate`
- `lastModifiedDate`


## Floor
It models the floor of a building. Its only required property is `floorNumber`.

## Room
It models the rooms in a building. Its required fields are:
- `roomNumber`
- `roomName`
- `floor`

## Donor
It models the organization which donates items. Its required field is `name`.


# Relationship Between Models

It becomes clear after seeing the ERD diagram. Here's a short explanation.

- A `Category` contains multiple `Type`.
- A `Type` contains multiple `Product`.
- A `Product` contains multiple `SubProduct`.
- A `Floor` contains multiple `Room`.
- A `Room` contains multiple `Product`.
- A `Donor` may donate multiple `Product`.

