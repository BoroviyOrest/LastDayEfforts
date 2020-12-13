import React from 'react';
import history from './history';
import {Router, Switch} from 'react-router-dom';
import {PublicRoute} from './PublicRoute';
import {RegistrationContainer} from "../containers/RegistrationContainer";
import {LoginContainer} from "../containers/LoginContainer";
import {NotFound} from "../components/NotFound";
import {GalleryPage} from "../components/client/GalleryPage";
import {RawImagePageContainer} from "../containers/client/RawImagePageContainer";
import {ClientStatsContainer} from "../containers/admin/ClientStatsContainer";
import {MlApiStatsContainer} from "../containers/admin/MlApiStatsContainer";


export const routes = (
    <Router history={history}>
        <Switch>
            <PublicRoute path='/login' component={LoginContainer}/>
            <PublicRoute path='/register' component={RegistrationContainer}/>
            <PublicRoute path='/gallery' component={GalleryPage}/>
            <PublicRoute path='/raw_image/:id' component={RawImagePageContainer}/>
            <PublicRoute path='/admin/clients_stats' component={ClientStatsContainer}/>
            <PublicRoute path='/admin/ml_api_stats' component={MlApiStatsContainer}/>
            <PublicRoute path='*' component={NotFound}/>
        </Switch>
    </Router>
);
