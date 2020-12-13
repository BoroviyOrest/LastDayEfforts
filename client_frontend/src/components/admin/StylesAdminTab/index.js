import React from 'react';
import _ from 'lodash';
import {Col, Row, Typography, DatePicker, Button, Menu, Layout, Empty} from 'antd';
import {Bar} from 'react-chartjs-2';

const {Content, Sider} = Layout;
const {Title} = Typography;
const {RangePicker} = DatePicker;

export const StylesAdminTab = ({styleStats, stylesList}) => {
    let stylesContent;

    if (_.isEmpty(stylesList)) {
        stylesContent = (
            <Empty/>
        );
    } else {
        stylesContent = _.map(stylesList, (style) => {
            const {description, id} = style;
            return (
                <Menu.Item key={id}>{description}</Menu.Item>
            )
        });
    }
    const barData = {
        labels: ['2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19'],
        datasets: [
            {
                label: 'Style usage by days',
                backgroundColor: 'rgba(255,99,132,0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1,
                hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                hoverBorderColor: 'rgba(255,99,132,1)',
                scaleStartValue: 0,
                data: styleStats
            }
        ],
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                }
            }]
        }
    };

    return (
        <Row>
            <Sider width={200} style={{borderLeft: '1px solid #f0f2f5'}}>
                <Menu
                    mode="inline"
                    style={{height: '100%'}}
                >
                    {stylesContent}
                </Menu>
            </Sider>
            <Content style={{padding: '24px', background: '#fff'}}>
                <Row>
                    <Col span={12}>
                        <Bar
                            data={barData}
                            height={500}
                            options={{maintainAspectRatio: false}}
                        />
                    </Col>
                    <Col span={12} style={{padding: '0 24px'}}>
                        <Title level={2}>Styles managing and stats</Title>
                        <p>Please, select dates interval to build statistics</p>
                        <RangePicker/>
                        <Button type="primary" size='large' style={{display: 'block', marginTop: '20px'}}>
                            Apply datetime interval
                        </Button>
                    </Col>
                </Row>
            </Content>
        </Row>
    )
};
