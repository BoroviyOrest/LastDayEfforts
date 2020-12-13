import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {getToken} from '../helpers/storageFunctions';

export const PrivateRoute = ({component: Component, ...rest}) => {
    const routeComponent = (props) => (
        getToken()
            ? <Component {...props} />
            : <Redirect to='/login'/>
    );

    return <Route {...rest} render={routeComponent}/>;
};
