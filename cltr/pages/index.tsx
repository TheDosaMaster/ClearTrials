import React, { useEffect , useState } from "react";


function index() {
  useEffect(() => {
  fetch("http://127.0.0.1:8080/solve")
  .then((response) => response.json())
  .then((data) =>
     {console.log(data);});
  }, []);
  return <div>index</div>;

}
export default index; 