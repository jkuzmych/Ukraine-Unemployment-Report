//datatype to work with jsons
export type ChartDataBucket = {
    [key: string]: number,
};

export type KeyConfig = {
    [key: string]: {
        label: string,
        color?: string,
    },
}

export type AxesConfig = {
    x: {
        label: string,
    },
    y: {
        label: string,
        suffix: string,
    },
};

export type ChartEncoding ={
    xKey: string,
    kind: string,
    unit: string,
    series: KeyConfig,
};

export type ChartData = {
    data: ChartDataBucket[],
    encoding: ChartEncoding,
    axes: AxesConfig,
    visibleByDefault: string[],

};

