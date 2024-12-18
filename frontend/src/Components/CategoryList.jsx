import React, { useState, useEffect} from 'react';

import ApiService from '../Services/ApiService';
import FetchClient from '../ServiceClients/FetchClient';

const CategoryList = () => {
  const [categoryList, setCategoryList] = useState([]);

  useEffect(() => {
    const apiService = new ApiService(FetchClient);

    const fetchCategories = async () => {
      try {
        const categoryList = await apiService.getCategories();
        setCategoryList(categoryList);
      } catch (error) {
        console.log(error);
      }
    }

    fetchCategories()
  }, [])

  return (
    <div>
      <h1>Categories: </h1>
      {categoryList.map((category, index) => (
        <p key={index}>{category.name}</p>
      ))}
    </div>
  )
}

export default CategoryList