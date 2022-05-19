import axios from "axios";
import React, {useEffect, useState} from 'react';
import toast from "react-hot-toast";

const base_url = "https://scarfly.ir/api"

const getData = async (listProductID) => {
    console.log("Get data")

    let url = base_url + '/products/list/?';
    for (let i = 0; i < listProductID.length; i++) {
        url += 'productID=' + listProductID[i] + '&'
    }
    return await axios.get(url);
}

function Carousel(listProductID) {
    console.log("Carousel")

    const [imgProduct, setImageProduct] = useState([]);
    useEffect(() => {
            const initialImgProduct = [];

            getData(listProductID).then((res) => {
                if (res && res.status === 200) {
                    const result = res.data.results
                    for (let i = 0; i < result.length; i++) {
                        initialImgProduct.push(result[i].image);
                    }
                    return true;
                } else {
                    console.log(res)
                    console.log(res.data)
                    toast.error('خطایی رخ داد .\n دوباره سعی کنید.');
                    return false;
                }
            }).then(isDone => {
                if (isDone) {
                    setImageProduct(initialImgProduct);
                }
            })
        }, []
    )

    console.log("end re-render")
    return (
        <div id="productDetail" className="rounded-2xl bg-white gap-4 flex flex-col w-100">
            <div className="container">
                <div id="myCarousel" className="carousel slide" data-ride="carousel">

                    <ol className="carousel-indicators">
                        {imgProduct.map((img, i) => (
                            <li key={i} data-target="#myCarousel" data-slide-to={i}
                                className={`${i === 0 ? 'active' : ''}`}/>
                        ))}
                    </ol>

                    <div className="carousel-inner">
                        {imgProduct.map((img, i) => (
                            <div key={i} className={`item w-100 ${i === 0 ? 'active' : ''}`}>
                                <img src={img} className="w-100 h-auto"/>
                            </div>
                        ))}
                    </div>

                    <a className="left carousel-control" href="#myCarousel" data-slide="prev">
                        <span className="glyphicon glyphicon-chevron-left"/>
                        <span className="sr-only">Previous</span>
                    </a>
                    <a className="right carousel-control" href="#myCarousel" data-slide="next">
                        <span className="glyphicon glyphicon-chevron-right"/>
                        <span className="sr-only">Next</span>
                    </a>
                </div>
            </div>
        </div>
    )
}

export default Carousel