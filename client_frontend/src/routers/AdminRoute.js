import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {isAdmin} from '../helpers/storageFunctions';

export const AdminRoute = ({component: Component, ...rest}) => {
    const isAllowed = isAdmin();
    const routeComponent = (props) => (
        isAllowed
            ? <Component {...props} />
            : <Redirect to='/gallery'/>
    );

    return <Route {...rest} render={routeComponent}/>;
};
