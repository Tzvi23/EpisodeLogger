import * as actionTypes from './actions';

const initialState = {
    userName: "Guest",
    password: "",
    removeStatus: {},
    userData: {}
};

const reducer = (state = initialState, action) =>{
    switch(action.type){
        case actionTypes.USER_LOGIN:
            return {
                ...state,
                userName: action.userName,
                password: action.password
            };
        case actionTypes.LOAD_DATA:
            return {
                ...state,
                userData: action.userData
            };
        default:
            return state;
    };
};

export default reducer;

