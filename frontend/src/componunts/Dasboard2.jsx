import {
  Card,
  CardBody,
  CardFooter,
  Typography,
  Button,
} from "@material-tailwind/react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../utils/Api";
 

export function Dasboard2() {

  const [productscount, setProductscount] = useState([]);
  const [citycount, setCitycount] = useState([]);
  const [categorycount, setCategorycount] = useState([]);

  useEffect(() => {
    fetchProductsData();
  }, []);

  const fetchProductsData = async () => {
    try {
      const response = await api.get("/googlemap_data");
      const products = response.data;

      // Extract unique cities
      const citys = products.map((product) => product.city);
      const uniqueCities = [...new Set(citys)];
      setCitycount(uniqueCities.length);

      // Extract unique categories
      const categories = products.map((product) => product.category);
      const uniqueCategories = [...new Set(categories)];
      setCategorycount(uniqueCategories.length);

      //product counter
      setProductscount( response.data.length);
     
    } catch (error) {
      console.error("Error fetching products:", error);
    }
    };

 return (<>
<div className="grid grid-cols-2 ">
      {/* Left Section - Services */}
      <div className="flex flex-col  pl-6">
        {/* Service Box */}
        <Card className="mt-6 w-96">
       <CardBody className="p-5">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="mb-4 h-12 w-10 text-gray-900"
        >
       <path d="M11.25 2.25a.75.75 0 01.5 0l8.25 3.375a.75.75 0 01.5.7v11.35a.75.75 0 01-.5.7l-8.25 3.375a.75.75 0 01-.5 0l-8.25-3.375a.75.75 0 01-.5-.7V6.325a.75.75 0 01.5-.7L11.25 2.25zm.25 1.5L4.5 6.325v10.35l7 2.87 7-2.87V6.325L11.5 3.75zm-6.25 3.75l6.25 2.5v7.5l-6.25-2.5v-7.5zm7.5 2.5l6.25-2.5v7.5l-6.25 2.5v-7.5z" />
        </svg>
        <Typography variant="h2" color="blue-gray" className="mb-2">
          Product Data
        </Typography>
        <Typography variant="h3" color="gray" className="mt-2">
          1200000
        </Typography>
        </CardBody>
        <CardFooter className="pt-0">
        <Link to="/dashboard/productdata-report" className="inline-block">
          <Button size="sm" variant="text" className="flex items-center gap-2" >
            View More
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="h-4 w-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3"
              />
            </svg>
          </Button>
        </Link>
      </CardFooter>
    </Card>

        {/* Service Items */}
      <Card className="mt-6 w-96">
      <CardBody>
        <Typography variant="h5" color="blue-gray" className="mb-2">
          Total Area scrapped
        </Typography>
          <Typography variant="h3" color="gray" className="mt-2">
          5248
        </Typography>
      </CardBody>
      </Card>
      <Card className="mt-6 w-96">
      <CardBody>
        <Typography variant="h5" color="blue-gray" className="mb-2">
          Total Category scrapped
        </Typography>
          <Typography variant="h3" color="gray" className="mt-2">
          941
        </Typography>
      </CardBody>
      </Card>
   </div>

      {/* Right Section - Listings */}
      <div className="flex flex-col ">
        {/* Product Box */}
        <Card className="mt-6 w-96">
      <CardBody className="p-5">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="mb-4 h-12 w-10 text-gray-900"
        >
       <path d="M11.25 2.25a.75.75 0 01.5 0l8.25 3.375a.75.75 0 01.5.7v11.35a.75.75 0 01-.5.7l-8.25 3.375a.75.75 0 01-.5 0l-8.25-3.375a.75.75 0 01-.5-.7V6.325a.75.75 0 01.5-.7L11.25 2.25zm.25 1.5L4.5 6.325v10.35l7 2.87 7-2.87V6.325L11.5 3.75zm-6.25 3.75l6.25 2.5v7.5l-6.25-2.5v-7.5zm7.5 2.5l6.25-2.5v7.5l-6.25 2.5v-7.5z" />
        </svg>
        <Typography variant="h2" color="blue-gray" className="mb-2">
          Listing Data
        </Typography>
        <Typography variant="h3" color="gray" className="mt-2">
          {productscount}
        </Typography>
      </CardBody>
      <CardFooter className="pt-0">
        <Link to="/dashboard/listingdata-report" className="inline-block">
          <Button size="sm" variant="text" className="flex items-center gap-2">
            View More
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="h-4 w-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3"
              />
            </svg>
          </Button>
        </Link>
      </CardFooter>
    </Card>

        {/* listing Items */}
       <Card className="mt-6 w-96">
      <CardBody>
        <Typography variant="h5" color="blue-gray" className="mb-2">
          Total Area scrapped
        </Typography>
        <Typography variant="h3" color="gray" className="mt-2">
          {citycount}
        </Typography>
      </CardBody>
      </Card> 
       <Card className="mt-6 w-96">
      <CardBody>
        <Typography variant="h5" color="blue-gray" className="mb-2">
          Total Category scrapped
        </Typography>
        <Typography variant="h3" color="gray" className="mt-2">
          {categorycount}
        </Typography>
      </CardBody>
      </Card> 
      </div>
    </div>
    
    </>
  );
}

export default Dasboard2;



