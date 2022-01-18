import {SHA256} from 'crypto-js'


interface DataObj{
    id: number,
    body: string,
    time: string
}

const data1:string = 'I rock!'
const dataObj : DataObj ={
    id:1,
    body:'DayumSon',
    time: new Date().getTime().toString().slice(0,-3)
};

const HashMe =(obj:DataObj|string):string=>{
    const result= SHA256(JSON.stringify(obj)).toString();
    console.log(result)
    return result
}

HashMe(dataObj);
HashMe(data1);


