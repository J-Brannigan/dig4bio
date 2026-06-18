from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

def generate_samples_plot(dfs: dict[str, pd.DataFrame]) ->plt.Figure:
    """
    Plot a sample of rows from each of the datasets/devices on one vertically stacked plot with the labelled fingerprint
    region
    
    Parameters
    ----------
    dfs: dict[str, pd.DataFrame]
        Dictionary of dataframes containing the device data to plot. The dictionary keys should be the device names
    
    Returns
    -------
    plt.Figure
        A figure object containing the vertically stacked sample plot for the datasets/devices    
    """

    device_names = dfs.keys()

    fig=plt.figure()
    gs = fig.add_gridspec(len(device_names), hspace=0)
    axs = gs.subplots(sharex=True, sharey=False)

    def plot_spectra_sample(ax, device:str) -> None:
        """Plot the sample spectra from one device on one axis"""

        df_to_show = dfs[device]

        # Datasets have different columns so spectral columns should be selected differently
        if device == 'transfer_plate':
            spectral_cols = df_to_show.columns[1:-4]
        elif device == '96_samples':
            spectral_cols = df_to_show.columns[1:]
        else:
            spectral_cols = df_to_show.columns[:-5]

        wavenumbers = spectral_cols.astype(float)
        df_sample = df_to_show.sample(10,random_state=90)
        spectra = df_sample[spectral_cols].to_numpy()

        ax.plot(wavenumbers,spectra.T,alpha=0.5)

        # 98th percentile to stop outliers affecting visibility
        ax.set_ylim(0, np.nanpercentile(spectra, 98))

        ax.text(0.75,0.65,device,transform=ax.transAxes,ha="right",va="top",fontsize=9,fontweight="bold")

    def add_fingerprint_region(fig, axs, x_1,x_2, **kwargs) -> None:
        """Add the fingerprint region vertical wavenumber lines and a label to the overall figure"""
        ax_ref = axs[-1]

        # Convert the two fingerprint boundary x-values from data coordinates
        # into display/pixel coordinates.
        x_display_1 = ax_ref.transData.transform((x_1, 0))[0]
        x_display_2 = ax_ref.transData.transform((x_2, 0))[0]

        # Convert display coordinates into figure-relative coordinates.
        # Figure coordinates run from 0 to 1 across the full figure.
        x_fig_1 = fig.transFigure.inverted().transform((x_display_1, 0))[0]
        x_fig_2 = fig.transFigure.inverted().transform((x_display_2, 0))[0]

        y0 = min(ax.get_position().y0 for ax in axs)
        y1 = max(ax.get_position().y1 for ax in axs)

        line_1 = Line2D([x_fig_1, x_fig_1],[y0, y1],transform=fig.transFigure,**kwargs)
        line_2 = Line2D([x_fig_2, x_fig_2],[y0, y1],transform=fig.transFigure,**kwargs)

        fig.add_artist(line_1)
        fig.add_artist(line_2)

        axs[0].text(1000,4000,'Fingerprint Region',color='red',fontweight="bold",ha='center')

    for ax, device in zip(axs, device_names):
        plot_spectra_sample(ax, device)

    # Hide all but bottom x axes
    for ax in axs:
        ax.label_outer()

    fig.supxlabel("Wavenumber $(cm^{-1})$")
    fig.supylabel("Intensity")
    fig.suptitle("10 Sample Spectra For each Dataset")

    fig.tight_layout()

    add_fingerprint_region(fig,axs,300,1800,color="red",linestyle="--",linewidth=1)

    axs[-1].set_xticks(np.arange(0,3501,250,))
    axs[-1].tick_params(axis="x", labelrotation=45)

    # To ensure fig isn't automatically displayed
    plt.close(fig)

    return fig