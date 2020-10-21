# -*- coding: utf-8 -*-

from ..init_fig import init_fig
from .plot_A_2D import plot_A_2D
from ...definitions import config_dict
from numpy import squeeze, split, max as np_max, where,array
from itertools import repeat


def plot_A_space(
    data,
    index_list=[0],
    t=None,
    t_index=0,
    is_deg=True,
    is_fft=False,
    is_spaceorder=False,
    r_max=100,
    fund_harm=None,
    is_norm=False,
    unit="SI",
    data_list=[],
    legend_list=[],
    color_list=[],
    linestyle_list=[],
    save_path=None,
    y_min=None,
    y_max=None,
    mag_max=None,
    is_auto_ticks=True,
    fig=None,
    subplot_index=None,
):
    """Plots a field as a function of space (angle)
    
    /!\ If relevant /!\ :
        - any change in Function.Plot.plot_A_space should be added in Method.Output.Output.plot.plot_A_space
        - any change in plot_A_space that is applicable to plot_A_time should be implemented in both      

    Parameters
    ----------
    data : Data
        a Data object
    index_list : list
        list of indices to take from a components axis
    t : float
        time value at which to slice
    t_index : int
        time index at which to slice
    is_deg : bool
        boolean indicating if the angle must be converted to degrees
    is_fft : bool
        boolean indicating if we want to plot the space-fft below the plot
    is_spaceorder : bool
        boolean indicating if we want to use the spatial order for the fft axis
    r_max : int
        maximum value of the wavenumber for the fft axis
    fund_harm : float
        frequency of the fundamental harmonic
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    data_list : list
        list of Data objects to compare
    legend_list : list
        list of legends to use for each Data object (including reference one) instead of data.name
    color_list : list
        list of colors to use for each Data object
    linestyle_list : list
        list of linestyle to use for each Data object (ex: "-", "dotted")
    save_path : str
        path and name of the png file to save
    y_min : float
        minimum value for the y-axis
    y_max : float
        maximum value for the y-axis
    mag_max : float
        maximum alue for the y-axis of the fft
    is_auto_ticks : bool
        in fft, adjust ticks to wavenumbers (deactivate if too close)
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    """

    # Set plot
    is_show_fig = True if fig is None else False
    (fig, axes, patch_leg, label_leg) = init_fig(fig, shape="rectangle")
    data_list2 = [data] + data_list
    if legend_list == []:
        legend_list = [d.name for d in data_list2]
    curve_colors = config_dict["PLOT"]["COLOR_DICT"]["CURVE_COLORS"]
    phase_colors = config_dict["PLOT"]["COLOR_DICT"]["PHASE_COLORS"]
    legends = []
    colors = []
    linestyles = []
    n_phase = len(index_list)
    list_str = None
    for i, d in enumerate(data_list2):
        is_components = False
        for axis in d.axes:
            try:
                if axis.is_components:
                    is_components = True
                    legends += [
                        legend_list[i] + ": " + axis.values.tolist()[j]
                        for j in index_list
                    ]
                    colors += [phase_colors[i * n_phase + j] for j in range(n_phase)]
                    linestyles += list(repeat("-", n_phase))
                    list_str = axis.name
            except:
                is_components = False
        if not is_components:
            legends.append(legend_list[i])
            colors.append(curve_colors[i])
            linestyles.append("-")
    if color_list == []:
        color_list = colors
    if linestyle_list == []:
        linestyle_list = linestyles
    if unit == "SI":
        unit = data.unit
    if is_norm:
        ylabel = r"$\frac{" + data.symbol + "}{" + data.symbol + "_0}\, [" + unit + "]$"
    else:
        ylabel = r"$" + data.symbol + "\, [" + unit + "]$"

    # Prepare the extractions
    if is_deg:
        a_str = "angle{°}"
        xlabel = "Angle [°]"
    else:
        a_str = "angle"
        xlabel = "Angle [rad]"
    if t != None:
        t_str = "time=" + str(t)
    else:
        t_str = "time[" + str(t_index) + "]"
        
    # Title string
    if list_str is not None:
        title = data.name + " over space for " + list_str + str(index_list)
    else:
        title = data.name + " over space for " + t_str            
 
    if data_list != []:
        title = "Comparison of " + title

    # Extract the fields
    Xdatas = []
    Ydatas = []
    if list_str is not None:
        for d in data_list2:
            results = data.get_along(
                a_str,
                t_str,
                list_str + str(index_list),
                unit=unit,
                is_norm=is_norm,
            )
            Xdatas.append(results["angle"])
            Ydatas.append(results[data.symbol])
    else:
        for d in data_list2:
            results = data.compare_along(
                a_str, t_str, data_list=data_list, unit=unit, is_norm=is_norm
            )
            Xdatas.append(results["angle"])
            Ydatas.append(results[data.symbol])
    
    # Nicely spaced ticks if angle in degrees
    angle = Xdatas[0]
    if is_deg and round(np_max(angle) / 6) % 5 == 0:
        xticks = [i * round(np_max(angle) / 6) for i in range(7)]
    else:
        xticks = None
        
    Ydata = []
    for d in Ydatas:
        if d.ndim != 1:
            axis_index = where(array(d.shape)==len(index_list))[0]
            if axis_index.size > 1:
                print("WARNING, several axes with same dimensions")
            Ydata += split(d, len(index_list), axis=axis_index[0])
        else:
            Ydata += [d]
    Ydata = [squeeze(d) for d in Ydata]

    # Plot the original graph
    ax = plot_A_2D(
        Xdatas,
        Ydata,
        legend_list=legends,
        color_list=color_list,
        linestyle_list=linestyle_list,
        fig=fig,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        y_min=y_min,
        y_max=y_max,
        xticks=xticks,
        save_path=save_path,
        subplot_index=subplot_index,
    )

    if is_fft:
        if "dB" in unit:
            unit_str = (
                "[" + unit + " re. " + str(data.normalizations["ref"]) + data.unit + "]"
            )
        else:
            unit_str = "[" + unit + "]"
        if data_list == []:
            title = "FFT of " + data.name
        else:
            title = "Comparison of " + data.name + " FFT"
        if data.symbol == "Magnitude":
            ylabel = "Magnitude " + unit_str
        else:
            ylabel = r"$|\widehat{" + data.symbol + "}|$ " + unit_str
        legend_list = [legend_list[0]] + [legend_list[-1]]

        Xdatas = []
        Ydatas = []
        if is_spaceorder:
            order_max = r_max / data.normalizations.get("space_order")
            xlabel = "Space order []"
            for d in data_list2:
                results = d.get_magnitude_along(
                    "wavenumber=[0," + str(order_max) + "]{space_order}",
                    t_str,
                    unit=unit,
                    is_norm=False,
                )
                Xdatas.append(results["wavenumber"])
                Ydatas.append(results[data.symbol])

        else:
            xlabel = "Wavenumber []"
            for d in data_list2:
                results = d.get_magnitude_along(
                    "wavenumber=[0," + str(r_max) + "]",
                    t_str,
                    unit=unit,
                    is_norm=False,
                )
                Xdatas.append(results["wavenumber"])
                Ydatas.append(results[data.symbol])
                
        wavenumber = Xdatas[0]

        if is_auto_ticks:
            indices = [ind for ind, y in enumerate(Ydatas[0]) if abs(y) > abs(0.01 * np_max(y))]
            xticks = wavenumber[indices]
        else:
            xticks = None

        plot_A_2D(
            Xdatas,
            Ydatas,
            legend_list=legend_list,
            color_list=color_list,
            linestyle_list=linestyle_list,
            fig=fig,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            type="bargraph",
            is_fund=True,
            fund_harm=fund_harm,
            y_max=mag_max,
            xticks=xticks,
            save_path=save_path,
        )

    if is_show_fig:
        fig.show()

    return ax
