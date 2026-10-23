/* REFPROP WATER.FLD v9.1 liquid-water fit at 101325 Pa.
 * Valid material temperature: 280 <= T <= 360 K.
 * Fits use x=(T-320)/40. Viscosity is exp(poly(x)).
 * No REFPROP DLL or external data file is needed during Fluent runs.
 * Cp and sensible enthalpy use the same polynomial. */
#include "udf.h"
#include <math.h>

#define WATER_TMIN 280.0
#define WATER_TMAX 360.0
#define WATER_NCOEF 8

static const double a_rho[WATER_NCOEF] = {
    989.4268704445951,
    -17.2499310366177,
    -5.44952039388111,
    0.8937461803438548,
    -0.2773582838633109,
    0.08628327753856567,
    -0.0424144765546545,
    0.01632650404645985
 };

static const double a_mu[WATER_NCOEF] = {
    -7.458144075726878,
    -0.6951542213971276,
    0.1546757900129285,
    -0.0401270818222776,
    0.01304476555605037,
    -0.004742215165989559,
    0.002097235476552828,
    -0.0007100029935473179
 };

static const double a_k[WATER_NCOEF] = {
    0.6369958912265128,
    0.04716101414130876,
    -0.01443810014348025,
    0.0019237580078174,
    -0.0007844097491474464,
    0.0003971492574949907,
    -0.0002251086922119273,
    8.486012343397388e-05
 };

static const double a_cp[WATER_NCOEF] = {
    4180.533095451139,
    9.168841573868214,
    14.28568175145558,
    -5.396174034390482,
    5.422292111368467,
    -2.463169671595042,
    1.391017947807678,
    -0.608097729351933
 };

static real water_poly(real T, const double *a)
{
    real x=(T-320.0)/40.0;
    real value=a[WATER_NCOEF-1];
    int i;
    for(i=WATER_NCOEF-2;i>=0;--i) value=value*x+a[i];
    return value;
}

static void water_check_temperature(real T)
{
    if (!(T>=WATER_TMIN && T<=WATER_TMAX))
        Error("Water UDF: T=%g K outside 280-360 K; extend the fit before use.\n",T);
}

/* Integral of fitted Cp with respect to T; its additive constant is arbitrary.
 * Endpoint Cp extension is only for enthalpy reference temperatures outside
 * the fit interval. Material temperatures are checked separately. */
static real water_h_primitive(real T)
{
    real Tb=T;
    real x, value;
    int i;
    if(Tb<WATER_TMIN) Tb=WATER_TMIN;
    if(Tb>WATER_TMAX) Tb=WATER_TMAX;
    x=(Tb-320.0)/40.0;
    value=a_cp[WATER_NCOEF-1]/WATER_NCOEF;
    for(i=WATER_NCOEF-2;i>=0;--i)
        value=value*x+a_cp[i]/(i+1.0);
    return 40.0*x*value+(T-Tb)*water_poly(Tb,a_cp);
}

DEFINE_PROPERTY(water_rp_density,c,t)
{
    real T=C_T(c,t);
    water_check_temperature(T);
    return water_poly(T,a_rho); /* kg/m3 */
}

DEFINE_PROPERTY(water_rp_viscosity,c,t)
{
    real T=C_T(c,t);
    water_check_temperature(T);
    return exp(water_poly(T,a_mu)); /* Pa.s */
}

DEFINE_PROPERTY(water_rp_conductivity,c,t)
{
    real T=C_T(c,t);
    water_check_temperature(T);
    return water_poly(T,a_k); /* W/(m.K) */
}

DEFINE_SPECIFIC_HEAT(water_rp_cp,T,Tref,h,yi)
{
    water_check_temperature(T);
    *h=water_h_primitive(T)-water_h_primitive(Tref); /* J/kg */
    return water_poly(T,a_cp); /* J/(kg.K) */
}

DEFINE_ON_DEMAND(water_rp_check)
{
#if !RP_NODE
    Message("RP_CHECK 300K rho=%.12g cp=%.12g mu=%.12g k=%.12g\n",
        water_poly(300.,a_rho),water_poly(300.,a_cp),
        exp(water_poly(300.,a_mu)),water_poly(300.,a_k));
    Message("RP_CHECK 330K rho=%.12g cp=%.12g mu=%.12g k=%.12g dh300_330=%.12g\n",
        water_poly(330.,a_rho),water_poly(330.,a_cp),
        exp(water_poly(330.,a_mu)),water_poly(330.,a_k),
        water_h_primitive(330.)-water_h_primitive(300.));
#endif
}
