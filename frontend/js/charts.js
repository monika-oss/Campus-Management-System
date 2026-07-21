const charts = {
  renderColumnChart(containerId, data, xField, yField, color = '#2563EB') {
    const container = document.getElementById(containerId);
    if (!container || !window.G2Plot || !window.G2Plot.Column) return;
    
    container.innerHTML = '';
    const chart = new window.G2Plot.Column(containerId, {
      data,
      xField,
      yField,
      color,
      label: {
        position: 'middle',
        style: { fill: '#FFFFFF', opacity: 0.6 },
      },
      xAxis: {
        label: { autoHide: true, autoRotate: false },
      },
      meta: {
        [yField]: { alias: 'Count' },
      },
    });
    chart.render();
    return chart;
  },

  renderLineChart(containerId, data, xField, yField, color = '#10B981') {
    const container = document.getElementById(containerId);
    if (!container || !window.G2Plot || !window.G2Plot.Line) return;

    container.innerHTML = '';
    const chart = new window.G2Plot.Line(containerId, {
      data,
      xField,
      yField,
      color,
      point: {
        size: 5,
        shape: 'diamond',
      },
      label: {
        style: { fill: '#aaa' },
      },
    });
    chart.render();
    return chart;
  },

  renderDonutChart(containerId, data, angleField, colorField) {
    const container = document.getElementById(containerId);
    if (!container || !window.G2Plot || !window.G2Plot.Pie) return;

    container.innerHTML = '';
    const chart = new window.G2Plot.Pie(containerId, {
      data,
      angleField,
      colorField,
      radius: 0.8,
      innerRadius: 0.6,
      label: {
        type: 'inner',
        offset: '-50%',
        content: '{value}',
        style: { textAlign: 'center', fontSize: 14 },
      },
      interactions: [{ type: 'element-selected' }, { type: 'element-active' }],
      statistic: {
        title: false,
        content: {
          style: { whiteSpace: 'pre-wrap', overflow: 'hidden', textOverflow: 'ellipsis' },
          content: 'Total\n' + data.reduce((a, b) => a + b[angleField], 0),
        },
      },
      color: ['#10B981', '#F59E0B', '#EF4444'], // Success, Warning, Danger colors mapped to Approved, Pending, Rejected usually
    });
    chart.render();
    return chart;
  },

  renderAreaChart(containerId, data, xField, yField) {
    const container = document.getElementById(containerId);
    if (!container || !window.G2Plot || !window.G2Plot.Area) return;

    container.innerHTML = '';
    const chart = new window.G2Plot.Area(containerId, {
      data,
      xField,
      yField,
      color: '#2563EB',
      areaStyle: () => {
        return {
          fill: 'l(270) 0:#ffffff 0.5:#7ec2f3 1:#2563EB',
        };
      },
    });
    chart.render();
    return chart;
  }
};
