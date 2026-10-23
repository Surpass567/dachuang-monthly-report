#include "udf.h"
#include <math.h>
#include <stdlib.h>

#define Q_INITIAL 1.0e6
#define Q_MEAN 6.5e6
#define Q_PEAK 1.0e7
#define TAU 20.0
#define FLUCT 0.05
#define SPIKE_PROB 0.002
#define SPIKE_TIME 0.05

static real random_uniform(void)
{
    return (real)rand() / (real)RAND_MAX;
}

DEFINE_PROFILE(microchannel_heat_flux, thread, index)
{
    face_t f;
    real time;
    real q;
    real fluctuation;
    static int spike_flag = 0;
    static real spike_start = 0.0;

    time = CURRENT_TIME;

    if (time < 5.0 * TAU)
    {
        q = Q_MEAN
            - (Q_MEAN - Q_INITIAL) * exp(-time / TAU);
    }
    else
    {
        fluctuation = (2.0 * random_uniform() - 1.0)
                      * FLUCT * Q_MEAN;
        q = Q_MEAN + fluctuation;
    }

    if (spike_flag == 0 && random_uniform() < SPIKE_PROB)
    {
        spike_flag = 1;
        spike_start = time;
    }

    if (spike_flag == 1)
    {
        if (time - spike_start < SPIKE_TIME)
        {
            q = Q_PEAK * (0.8 + 0.2 * random_uniform());
        }
        else
        {
            spike_flag = 0;
        }
    }

    begin_f_loop(f, thread)
    {
        F_PROFILE(f, thread, index) = q;
    }
    end_f_loop(f, thread)
}
