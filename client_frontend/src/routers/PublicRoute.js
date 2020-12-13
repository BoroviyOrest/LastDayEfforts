import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {getToken} from '../helpers/storageFunctions';

export const PublicRoute = ({component: Component, ...rest}) => {
    const routeComponent = (props) => (
        getToken()
            ? <Redirect to='/gallery'/>
            : <Component {...props} />
    );

    return <Route {...rest} render={routeComponent}/>;
};
