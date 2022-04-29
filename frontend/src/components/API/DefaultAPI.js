import axios from 'axios'

const base_url = 'https://scarfly.ir/api';

export async function verifyUser() {
    console.log("Verify User")

    const refreshToken = localStorage.getItem('refresh');
    if (refreshToken != null) {
        const refreshResponse = await axios.post(
            base_url + `/accounts/refresh/`,
            JSON.stringify({"refresh": refreshToken}),
            {headers: {'content-type': 'application/json'}});
        if (refreshResponse.status === 200) {
            setTokens(refreshResponse.data.access, refreshToken);
            return true
        }
    }
    return false
}


export async function Retrieve(input) {
    console.log("Retrieve")

    await axios.get(`${base_url}/orders/${input}/`,
        {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}}).then(res => {
    }).catch(err => {
        Refresh().then(Retrieve(input))
    })


export async function refresh() {
    console.log("Refresh");


export async function Refresh() {
    if (localStorage.getItem('refresh')) {
        let response = await axios.post(`${base_url}/accounts/refresh/`,
            JSON.stringify({"refresh": localStorage.getItem('refresh')}),
            {headers: {'content-type': 'application/json'}})

        setTokens(response.data.access)
        return
    }
}

export async function login(input) {
    console.log("Login")

    let response = await axios.post(base_url + '/accounts/login/',
        JSON.stringify({"phone_number": input.toString()}),
        {headers: {'content-type': 'application/json'}})
        .then(response => {
            if (response.status === 200) {
                setTokens(response.data.access, response.data.refresh)
                return true
            }
        }).catch(err => {
            if (err.response.status === 400) {
                return register(input)
            }
            console.log(err)
            console.log(err.response)
            console.log(err.response.data)
        })
    return response === true
}

export const register = async (input) => {
    console.log("Register")

    const response = await axios.post(base_url + '/accounts/register/',
        JSON.stringify({"phone_number": input.toString()}),
        {headers: {'content-type': 'application/json'}}
    ).then(response => {
        if (response.status === 200) {
            setTokens(response.data.access, response.data.refresh)
            return true
        }
    }).catch(err => {
        console.log(err)
        console.log(err.response)
        console.log(err.response.data)
    })
    return response === true
}


const setTokens = (access, refresh) => {
    access && localStorage.setItem('access', access)
    refresh && localStorage.setItem('refresh', refresh)
}


export const verify = async () => {
    console.log("Verify")
    await Refresh()
    if (localStorage.getItem('access')) {
        return await axios.get(base_url + '/accounts/verify/', {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}})
    }
}

export const createOrder = async (input) => {
    return await axios.post(base_url + '/orders/create/', input, {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}})
}


