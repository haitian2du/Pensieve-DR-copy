import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update( {'font.size': 6} )

# prefix_1 = "../results/jump-action-test-fixed-penalty/2-bad-trace-original-16/trace-1052/train_maxBW_60-22500/test-on-"
prefix_1 = "../results/pensieve-mpc-lesley-test-3/test-on-"

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

# prefix_1 = "./results/synthetic-test/Ts-test-new/train_Ts_100/test-on-"
# prefix_2 = "./results/synthetic-test/Ts-test-new/train_Ts_80/test-on-"
# prefix_3 = "./results/synthetic-test/Ts-test-new/train_Ts_30/test-on-"
# prefix_4 = "./results/synthetic-test/Ts-test-new/train_Ts_2/test-on-"
# prefix_5 = "./results/synthetic-test/Ts-test-new/mpc/test-on-"


FS = []
for i in range(1, 99):
    FS.append(str(i))


def folder_name_from(unique, prefix):
    suffix = "/seed_1/"
    folder = prefix + unique +suffix
    return folder


RESULTS_FOLDER_1 = [folder_name_from( x, prefix_1 ) for x in FS] # jump-action

RESULTS_FOLDERs = [RESULTS_FOLDER_1]

NUM_BINS = 100
BITS_IN_BYTE = 8.0
MILLISEC_IN_SEC = 1000.0
M_IN_B = 1000000.0
VIDEO_LEN = 48
K_IN_M = 1000.0
REBUF_P = 4.3
SMOOTH_P = 1
COLOR_MAP = plt.cm.jet  # nipy_spectral, Set1,Paired
# SCHEMES = ['sim_mpc', 'sim_rl']
SCHEMES = ['sim_rl']


def main():
    all_mean_reward = []
    all_var_mean = []


    for RESULTS_FOLDER in RESULTS_FOLDERs:
        mean_reward_plot = []
        error_bar_plot = []
        for each_folder in RESULTS_FOLDER:
            log_files = listdir_nohidden( each_folder )

            time_all = {}
            raw_reward_all = {}

            for scheme in SCHEMES:
                time_all[scheme] = {}
                raw_reward_all[scheme] = {}

            for log_file in log_files:
                time_ms = []
                reward = []

                with open( each_folder + log_file, 'r' ) as f:
                    for line in f:
                        parse = line.split()
                        if len( parse ) <= 1:
                            break
                        time_ms.append( float( parse[0] ) )
                        reward.append( float( parse[6] ) )
                    # print( reward, "--------------------" )

                time_ms = np.array( time_ms )
                time_ms -= time_ms[0]

                for scheme in SCHEMES:
                    if scheme in log_file:
                        time_all[scheme][log_file[len( 'log_' + str( scheme ) + '_' ):]] = time_ms
                        raw_reward_all[scheme][log_file[len( 'log_' + str( scheme ) + '_' ):]] = reward
                        break

            # ---- ---- ---- ----
            # Reward records
            # ---- ---- ---- ----

            log_file_all = []
            reward_all = {}
            mean_all = []
            for scheme in SCHEMES:
                reward_all[scheme] = []

            for l in time_all[SCHEMES[0]]:
                schemes_check = True
                # all schemes must pass the check
                for scheme in SCHEMES:
                    if l not in time_all[scheme] or len( time_all[scheme][l] ) < VIDEO_LEN:
                        schemes_check = False
                        break
                if schemes_check:
                    log_file_all.append( l )
                    for scheme in SCHEMES:
                        reward_all[scheme].append( np.sum( raw_reward_all[scheme][l][1:VIDEO_LEN] ) / VIDEO_LEN )
                        mean = np.mean(raw_reward_all[scheme][l][1:VIDEO_LEN]) / VIDEO_LEN
                        mean_all.append(mean)



            for scheme in SCHEMES:
                mean_reward = np.mean( reward_all[scheme] )
                error_bar = np.std( mean_all )
                #print(error_bar)


            mean_reward_plot.append( mean_reward )
            error_bar_plot.append(error_bar)

        all_mean_reward.append(mean_reward_plot)
        all_var_mean.append(error_bar_plot)

    y_pensieve = all_mean_reward[0]
    y_pensieve_err = all_var_mean[0]

    print(y_pensieve, "-----")
    print(y_pensieve_err)

    # pensieve=[-2.638011565910128 ,-2.3581829309793285 ,-0.6226640856430276 ,-0.5599410623141032 ,-0.17301013431086673 ,
    #  -2.5277862970712563 ,-1.250415448800559 ,0.2725066055252583 ,1.552877088000572 ,2.4589971343487034 ,
    #  1.9153447777222237 ,1.9510134865992617 ,1.3010671990014198 ,-1.3881364972009314 ,-2.1567115402286903 ,
    #  1.0113208530917561 ,1.5219771276661844 ,3.116204884871475 ,1.1998087255967134 ,0.5155684272838836 ,
    #  -2.6504562034319923 ,2.643555124575382 ,4.877353552336306 ,2.7329960064278516 ,3.9955227935975524 ,
    #  3.3720445287008483 ,6.315338944551699 ,7.878656130892648 ,4.636032574197276 ,6.493192875001842 ,6.656459309039532 ,
    #  6.586855064814195 ,10.058829449441525 ,10.409593964191659 ,10.593192093267175 ,12.005009033237808 ,
    #  8.429483482192335 ,13.414659414053576 ,9.823018491202046 ,12.757451692185434 ,13.38422834238449 ,
    #  11.352241858042516 ,8.726852688052395 ,15.023662802045507 ,16.2687731405066 ,13.601777449663382 ,
    #  16.354316080993193 ,14.424768909997875 ,14.705083586802248 ,15.128061924769215 ,17.728581126082947 ,
    #  13.893855846819685 ,16.961471616271755 ,19.879303511257593 ,18.3481145550788 ,14.227126455599954 ,
    #  18.477646781496396 ,16.40374981422838 ,19.720055946719707 ,16.720387555379393 ,9.367716209386446 ,
    #  18.185136442826714 ,19.863144024776233 ,20.99359424566746 ,18.927731917574796 ,18.84261902006649 ,
    #  19.544016651912763 ,16.470206414436518 ,18.292268971050195 ,18.749963289459505 ,22.715428771057656 ,
    #  16.352866183043623 ,15.42638857951227 ,16.55760768282532 ,17.50379873648478 ,21.249755379395566 ,
    #  23.53580523990924 ,20.886764239805093 ,17.772662526443526 ,22.327681887446488 ,23.303716651316087 ,
    #  15.981547333057465 ,18.937356534289773 ,21.562869391376985 ,23.039673137041582 ,23.413703077497566 ,
    #  19.01518093586355 ,22.057420765533937 ,24.58101589866711 ,24.43023142996174 ,17.077990253517804 ,
    #  22.26821002758611 ,25.80335510874595 ,22.22784528105106 ,23.800607285473784 ,21.537251807935313 ,
    #  25.78843456204915 ,22.744721519698178]
    # pensieve_err=[0.13457031621083432 ,0.25148744140511675 ,0.13211277205553032 ,0.17476308733861226 ,0.14342910646161255 ,
    #  0.3494347144552278 ,0.22572912047101087 ,0.19754805462148142 ,0.10658691332127013 ,0.10985355588448097 ,
    #  0.13097242273753282 ,0.14331311508175842 ,0.2587230452490283 ,0.4397129436060835 ,0.4220826810752634 ,
    #  0.30515841884799233 ,0.29834493369858384 ,0.14871259161782105 ,0.28655434752796693 ,0.4007147482441826 ,
    #  0.5950736160716339 ,0.27704148633536546 ,0.16230729560794827 ,0.30346804696590873 ,0.33121460356643345 ,
    #  0.3222595192281725 ,0.20285960213928983 ,0.2209096512591602 ,0.41995886340366423 ,0.28432043487576897 ,
    #  0.37205521313963774 ,0.41547337025722003 ,0.2061867902229848 ,0.2224822154966358 ,0.27422806649148196 ,
    #  0.12141495449698832 ,0.3774453325231915 ,0.14685816191460405 ,0.37942992652058993 ,0.16386388023822418 ,
    #  0.2003252517496556 ,0.41084315158449086 ,0.6492289791771488 ,0.21313096270108275 ,0.1941124869421254 ,
    #  0.32112825182156646 ,0.3055639616328872 ,0.26213719753233145 ,0.17495871792587683 ,0.3705695176611979 ,
    #  0.16168442159485402 ,0.6027007815710811 ,0.17448565326575774 ,0.12451287043511726 ,0.21980357236509734 ,
    #  0.3076901868691808 ,0.17299946051796103 ,0.30082604374579813 ,0.10930902459143862 ,0.4630767268706905 ,
    #  0.8624441579041374 ,0.4023639143455437 ,0.23029974191931465 ,0.14681386664477797 ,0.18153337484224827 ,
    #  0.2917946424043265 ,0.27390123223925605 ,0.6432381835826397 ,0.4327085952868735 ,0.4882891667051864 ,
    #  0.10544283659319789 ,0.5415790019632087 ,0.438549943442747 ,0.4425464752262224 ,0.426130287674137 ,
    #  0.2739226995584988 ,0.17968381731082878 ,0.3185512306302788 ,0.332610459347314 ,0.18234855751948845 ,
    #  0.1802191701217188 ,0.5076342839194005 ,0.36160151835020826 ,0.2576341213705195 ,0.21403824046702233 ,
    #  0.2680046599898204 ,0.38785815674861607 ,0.2900872242623971 ,0.18525089962156485 ,0.218313296576137 ,
    #  0.6133558460592199 ,0.5802686535430841 ,0.11409174211659281 ,0.41209109049390974 ,0.241192153018885 ,
    #  0.6352168406484242 ,0.2775250399956155 ,0.2591644843513031]
    #
    # mpc = [-3.5643775168056333 ,-9.882537423269406 ,-12.960726826134739 ,-11.411109539150743 ,-11.289431695946039 ,
    #  -15.901228679168387 ,-14.484149413809819 ,-16.172521129568484 ,-12.129650171357378 ,-17.014609429380723 ,
    #  -14.08425199331088 ,-14.110911851766618 ,-11.060849154023312 ,-8.499046739818361 ,-16.80179447623993 ,
    #  -11.7558465359402 ,-11.816307719876534 ,-6.968693073082557 ,-10.919509081264266 ,-13.82707690744912 ,
    #  -11.934819294843207 ,-12.613061526199372 ,-4.837138270059935 ,-8.604956705325733 ,-0.897034995747767 ,
    #  -13.26214755161386 ,-5.660455016764103 ,3.097338672327723 ,-14.913863577790375 ,-11.138363038768636 ,
    #  -10.959890253158482 ,-1.607899477944937 ,0.7511708189348306 ,1.150378720807457 ,2.4415411593893994 ,
    #  4.0644331893484 ,4.716409104639429 ,5.004135658433153 ,-6.194500988832856 ,8.739929463092345 ,4.799798623474968 ,
    #  0.20296146196612305 ,7.409003402302488 ,3.255664164765016 ,1.8981058778715811 ,-2.8628514205148536 ,
    #  6.0656802539060015 ,9.145407969270696 ,6.86746072435264 ,11.471056503959206 ,13.610955503522378 ,
    #  0.568191659588368 ,6.056809423701426 ,11.903726846454381 ,10.310849605085057 ,3.3097483594516 ,12.813508547678463 ,
    #  5.226173674528475 ,15.223663410111055 ,10.319850486123698 ,10.648059277701709 ,9.8034506341489 ,
    #  16.644764883808303 ,13.36918839805766 ,4.032702666897455 ,3.4291817044507047 ,12.346699651670995 ,
    #  7.425996102678185 ,8.799506806741512 ,16.180108934318536 ,19.13364258756572 ,13.002346526546377 ,
    #  13.45342460670977 ,12.878622286650563 ,12.670211044567296 ,-0.4328603239181178 ,16.50713712970661 ,
    #  18.96621025315413 ,16.356744237711712 ,16.655794079415372 ,14.058612372040562 ,11.954932720559265 ,
    #  17.86573565860493 ,14.504722381665756 ,10.068775144159734 ,7.359161216889572 ,17.714417893961908 ,
    #  9.881031305146557 ,12.346071313051475 ,18.051843273483804 ,14.915261556645783 ,17.935300016285176 ,
    #  18.46685076982842 ,23.176710479401613 ,13.653993103624996 ,16.81125289525968 ,21.973068026732378 ,
    #  13.157065500111912]
    # mpc_err = [0.14036020995902918 ,0.3892891094207692 ,0.47304437247022296 ,0.52054932950283 ,0.39931023695599127 ,
    #  0.4784719897944055 ,0.5697270702706256 ,0.6857096591576263 ,0.519273996419327 ,0.8643026602154629 ,
    #  0.6212461862066727 ,0.6992578683933164 ,0.5567936419124927 ,0.5736014069046526 ,0.912528799113674 ,
    #  0.7155671859021207 ,0.532271190642242 ,0.4327722516776265 ,0.4523515882569341 ,0.7078375963682954 ,
    #  0.7188249937550018 ,0.6458467903071095 ,0.6325266683579689 ,0.690443092745314 ,0.448308699776235 ,
    #  0.7870934462487374 ,0.6884451644241496 ,0.4392790384436866 ,0.9286524981538627 ,0.9651047415101276 ,
    #  0.7826460888629243 ,0.7495662205899957 ,0.5862663071576854 ,0.48906522919226925 ,0.5010799592760087 ,
    #  0.48385895740229723 ,0.5107304933642488 ,0.4858456810177359 ,1.4022697971215685 ,0.37763228313574504 ,
    #  0.4142584369445896 ,0.777045151754384 ,0.4980278451420371 ,0.6591760806920459 ,0.7936569793061058 ,
    #  0.8646943141765869 ,0.5661698213488949 ,0.4821884181620692 ,0.5061741491904224 ,0.4953538441651295 ,
    #  0.5101233351524267 ,0.9389258757114907 ,0.6314955646983486 ,0.624086532172973 ,0.7652872969068608 ,
    #  0.6657839331791544 ,0.38795958281878107 ,0.7563581675661855 ,0.30525946983154234 ,0.7801452073586096 ,
    #  0.5723490401369067 ,0.6927670525632499 ,0.38523667064501754 ,0.5401153983375272 ,0.6571990779214567 ,
    #  0.7417586356720691 ,0.5882099468980847 ,0.7485995290182231 ,0.6795896760858989 ,0.4882663251680073 ,
    #  0.43858786755510304 ,0.7547802496529848 ,0.6158778869184189 ,0.6985298337516692 ,0.7239360863228433 ,
    #  1.0568212956059302 ,0.48369872650695156 ,0.588589297788753 ,0.4566528825811561 ,0.5147888122760205 ,
    #  0.5917090586609626 ,0.7774393542974446 ,0.5261295519474867 ,0.5875645688831242 ,0.7686006916443657 ,
    #  0.8233849423518758 ,0.6346639572604504 ,0.7120351735698619 ,1.0858901407537096 ,0.5210028885727005 ,
    #  0.838516229714512 ,0.8836652082507789 ,0.6089758350404808 ,0.5785067668827575 ,0.8354876568976488 ,
    #  0.72898831998681 ,0.6789307655653436 ,0.9283272107599132]

    # pensieve=[0.21714242982456156 ,0.6029200643274853 ,1.0965000000000003 ,1.3981731493155964 ,1.747168229775828 ,
    #  1.197750529001074 ,2.270015622807017 ,2.6973819487444093 ,3.269848348277461 ,3.410605215764568 ,4.146354166666666 ,
    #  4.056786604590625 ,4.751646903662556 ,4.245931614472317 ,5.194020833333334 ,5.391885310573794 ,5.510501549365634 ,
    #  5.714471978078534 ,6.18134520791479 ,6.463794626199226 ,6.818908468724096 ,6.977164076948945 ,6.647067011043224 ,
    #  7.636872384291486 ,7.320401100232127 ,9.219261661098274 ,9.045469261032189 ,9.891428883894699 ,10.955104749190102 ,
    #  11.139166666666668 ,12.17525 ,11.698221534559927 ,11.854137462927097 ,12.792327936720142 ,13.105841742068916 ,
    #  12.433321225125267 ,14.99997766822987 ,15.56550516055932 ,15.61579108674707 ,17.557216530575275 ,
    #  17.70147975026521 ,18.334519121088313 ,18.971195582334538 ,20.65057628943105 ,20.3836875 ,20.100133472992262 ,
    #  21.259749529863765 ,21.54354562844224 ,22.86473298018984 ,23.516666666666666 ,24.096988761735414 ,
    #  23.55692412280702 ,24.39941666666667 ,25.07669548988558 ,25.123104166666668 ,25.7863186637325 ,25.960520833333334 ,
    #  26.002645833333332 ,26.378 ,26.888375 ,26.628666666666668 ,27.049354166666667 ,27.150375000000004 ,
    #  26.960041666666665 ,26.91272916666667 ,27.385562500000002 ,27.427297329634186 ,27.46366666666667 ,
    #  27.63158509339839 ,27.662716991305388 ,27.684875 ,27.985375000000005 ,27.93600235006542 ,28.055229166666663 ,
    #  28.625361188315882 ,27.950680944779315 ,28.88334710386623 ,29.060987153621237 ,29.866187500000002 ,
    #  29.923456854212017 ,29.32851624802407 ,30.274703638981478 ,30.635265852214353 ,30.849915181946013 ,
    #  31.322145833333337 ,30.732709718933293 ,30.63613822038017 ,32.22617039967211 ,31.938725041341186 ,
    #  31.627482193283914 ,31.47852527545393 ,33.479800253857675 ,33.06620854862541 ,32.41255344560288 ,33.2419562712736 ,
    #  34.50474080342903 ,33.87787379666126 ,34.495965143678866]
    # pensieve_err = [0.01616690288116329 ,0.02220347226688305 ,0.002683655606231265 ,0.011650782854817365 ,0.018145903930005192 ,
    #  0.15482931911988487 ,0.03602042235318425 ,0.030163102942716388 ,0.02001371341501771 ,0.043574227060835705 ,
    #  0.010300324768987873 ,0.07176061727467926 ,0.011602678089710645 ,0.11054206416517438 ,0.013217494084053582 ,
    #  0.04340244630466182 ,0.04670324520185759 ,0.031815259704320344 ,0.031021944837977322 ,0.030046996268998084 ,
    #  0.02799617008938458 ,0.05732105340220716 ,0.08588958946067086 ,0.1479968625169035 ,0.08628202159403847 ,
    #  0.04283839245116756 ,0.06288017711545092 ,0.05175391308538149 ,0.036176610686608275 ,0.037681808241517366 ,
    #  0.04238948395861765 ,0.103762678130702 ,0.1131881909740334 ,0.08612056063600883 ,0.11258256819731607 ,
    #  0.12012688350643172 ,0.08671232179414985 ,0.07359013949392142 ,0.10062621100590152 ,0.052374053205781056 ,
    #  0.07995352414313094 ,0.06878838253194035 ,0.06614585493203788 ,0.06374971312530538 ,0.06813386850831507 ,
    #  0.07168192177381918 ,0.06037028769459911 ,0.08948097929301238 ,0.060499261906983376 ,0.05921053099457838 ,
    #  0.05554551240311349 ,0.0749423390843399 ,0.06475700368075425 ,0.06673801364289574 ,0.04881957710615759 ,
    #  0.06260249979434833 ,0.04684032830074933 ,0.04343453802224838 ,0.039494926271415515 ,0.035312611868427726 ,
    #  0.03690705671687314 ,0.03091258122723153 ,0.03129297531641028 ,0.03473301492267382 ,0.027842334727824727 ,
    #  0.025258617669897267 ,0.027234792817261495 ,0.03618544959196204 ,0.05207957078795574 ,0.03564212063757007 ,
    #  0.04604071356793655 ,0.04171576276041185 ,0.04512411221701715 ,0.04340401030416361 ,0.05100337227397267 ,
    #  0.0451932212024985 ,0.06009337915488151 ,0.06559803451564247 ,0.06438119634273713 ,0.08457766699441127 ,
    #  0.20541084848637167 ,0.058183829521795016 ,0.06913679873637822 ,0.07629477171470149 ,0.0688863052233672 ,
    #  0.13760325292749437 ,0.08217369397049754 ,0.07627715017053137 ,0.09873391414320469 ,0.09787138583897613 ,
    #  0.20462147281455412 ,0.08647510882786057 ,0.07881553900171627 ,0.14553352656081997 ,0.13917327581951638 ,
    #  0.17284809137525903 ,0.11414316816884229 ,0.1684594389416797]
    #
    # mpc=[-1.1734718038847114 ,-0.6066779770812801 ,-0.6038460669549589 ,0.17464824519575217 ,1.306800695964071 ,
    #  0.174599653881259 ,1.2026244262441985 ,2.041988410046171 ,2.2720283979863134 ,2.614350519924182 ,
    #  3.7937798322233216 ,2.8592072139013407 ,4.024446585622691 ,3.7018371853225402 ,4.423591276084131 ,
    #  4.351749278045717 ,4.464148452114383 ,5.487044869396795 ,5.367531750006177 ,5.987516908712576 ,6.526297004509974 ,
    #  6.029948367069885 ,5.737908404282649 ,7.292198673688458 ,6.636934854271467 ,8.242871534902509 ,8.497997334074135 ,
    #  9.536640834952168 ,8.526348843670608 ,10.293615983426662 ,10.630885608827366 ,11.06688147665904 ,
    #  12.151227249846478 ,11.310798526630931 ,12.471590567762732 ,12.644882539845382 ,14.736135212738352 ,
    #  15.16004199763491 ,16.0320799401304 ,16.41595796174972 ,17.721244163332805 ,18.182965965627574 ,
    #  18.697156336678148 ,19.71190546030697 ,19.413203051786503 ,19.11223661228162 ,20.903927102339182 ,
    #  21.595098053111524 ,21.759094766565713 ,22.90972613429794 ,22.155923864630587 ,23.151619998884158 ,
    #  22.57806565864214 ,22.161467286736443 ,23.334647060592275 ,24.934499110041298 ,24.815619486907757 ,
    #  23.362098428518717 ,24.3087931631133 ,25.741676419235482 ,25.047999172569625 ,26.34451355812608 ,
    #  25.30026805970572 ,24.947452212031592 ,25.51501073682205 ,25.97054166666667 ,25.04863184851334 ,25.23841808870316 ,
    #  26.188 ,26.31739583333334 ,26.377208668139495 ,26.22883333333333 ,25.441104166666666 ,25.695604166666666 ,
    #  26.31742246927014 ,25.952270833333333 ,27.60000789103553 ,27.59749381767217 ,26.613871987975834 ,
    #  26.71339552688349 ,27.25560181520018 ,27.81264252382893 ,27.922299252786903 ,27.683499713900293 ,
    #  27.862495191449497 ,28.72404060238559 ,29.256196383419688 ,27.47305203916435 ,28.833020833333336 ,
    #  28.887544583064336 ,29.100975254674424 ,29.06103786044605 ,29.656625 ,29.765274861323807 ,31.148666666666667 ,
    #  31.151973211369306 ,31.314048091178144 ,31.897355790460114]
    # mpc_err=[0.07129507253391498 ,0.07902429831605637 ,0.08605489252540141 ,0.09482126168577494 ,0.049512641334317854 ,
    #  0.11120794100074355 ,0.08813810359761336 ,0.05660795659752253 ,0.12311227704957686 ,0.0791721866615054 ,
    #  0.029523862061354916 ,0.11733963128852178 ,0.034890018255014116 ,0.06486023889451782 ,0.04658766730791681 ,
    #  0.07983307792071011 ,0.06548926340804158 ,0.026432327047639318 ,0.10112841393226153 ,0.0448046607647634 ,
    #  0.041901672224842236 ,0.13883550692946275 ,0.11008005318559436 ,0.11638788347786867 ,0.12470273724421878 ,
    #  0.07304610484581528 ,0.06804418929805418 ,0.05725530041274887 ,0.09543107996420164 ,0.05094124404310845 ,
    #  0.100726104413091 ,0.1301491309292848 ,0.0538573331241196 ,0.13526002700373307 ,0.12372240204983924 ,
    #  0.11141733360836828 ,0.09848933118110283 ,0.06565909296393328 ,0.05266935508804163 ,0.05984781913396363 ,
    #  0.06774226992578124 ,0.06270469979073533 ,0.06428639601919017 ,0.09386016631679531 ,0.13389700018410622 ,
    #  0.10005473991228427 ,0.06464934035963418 ,0.07415677525134698 ,0.08863464101740293 ,0.0652966545702235 ,
    #  0.09958975481963966 ,0.07191909328046929 ,0.08620421528741744 ,0.17440861185471895 ,0.08851622796918221 ,
    #  0.06347463104486036 ,0.07098899072851907 ,0.12541524697635767 ,0.08286644254858679 ,0.07009042424818815 ,
    #  0.08002458433935497 ,0.07111424685107144 ,0.08515472763745657 ,0.07566232561030284 ,0.08377189562385788 ,
    #  0.0793023214011176 ,0.1140410323188198 ,0.10327041045469325 ,0.08081080894008534 ,0.08295718203889872 ,
    #  0.10003383084679343 ,0.08591125396455598 ,0.09156012952558458 ,0.11736904532759874 ,0.09558919489533896 ,
    #  0.11232466491989995 ,0.10251969457499736 ,0.10134613302031732 ,0.08990570089724799 ,0.11025305075574972 ,
    #  0.11692786996800393 ,0.08582380546597516 ,0.09488692508965181 ,0.12823361333467445 ,0.09766244907561045 ,
    #  0.13199698679826277 ,0.12644782866873977 ,0.11758681941090274 ,0.1133008217702935 ,0.11979254542999122 ,
    #  0.14782007978380396 ,0.14163445534574107 ,0.129088097383277 ,0.1351947594988697 ,0.12822355972621502 ,
    #  0.18113353054875717 ,0.12019946284325292 ,0.1422596176656984]

    mpc=[-1.2630608838763466 ,-0.3615755530402465 ,-0.9364654051786279 ,0.20607987163718405 ,-0.8548647068395083 ,
     0.9188403380683252 ,1.6235719278974492 ,1.2273170024742777 ,0.5387668903716353 ,1.4954496531318187 ,
     3.464644680562626 ,2.8586004232737303 ,3.609047295409576 ,3.866870301514246 ,3.8966918358757914 ,3.41341205086922 ,
     4.472334039679534 ,5.148271946402956 ,4.754377113687229 ,5.586351590426655 ,5.17685316356808 ,6.596421039873061 ,
     6.767589124981721 ,5.86015473545428 ,6.785503415465902 ,5.40720506326872 ,8.2166783276958 ,8.639166508047932 ,
     8.350584567483478 ,7.961378470985477 ,8.395395957227677 ,8.305765308778625 ,11.017617272195823 ,
     10.538246656843135 ,12.268561448454637 ,13.292760417347143 ,12.480998732496873 ,14.617262847491856 ,
     14.952168782580403 ,15.023401581032251 ,14.54272619720042 ,18.07911343828927 ,17.19052756049878 ,
     18.947789436830146 ,17.866120887920165 ,19.18427469571048 ,19.969193978661067 ,20.283405144762643 ,
     20.955622732732717 ,20.99632016823061 ,22.8383524984032 ,21.86743909325784 ,22.05612603165296 ,21.360221951942727 ,
     23.205229166666673 ,23.145864879963337 ,24.151875 ,22.92124569258042 ,23.85413804454382 ,22.12887707905479 ,
     22.693589882205288 ,23.73340172709345 ,25.493503963991078 ,23.644810607256815 ,24.895338320128282 ,
     24.28462393549396 ,25.368993818541718 ,23.56084571645212 ,25.357020833333337 ,25.29887902214437 ,26.089375 ,
     24.849929238881785 ,24.115223264578702 ,25.440187499999997 ,25.81357621746809 ,26.11558794885831 ,
     25.1980117887439 ,26.321263329854858 ,25.43339884722513 ,24.90869724042935 ,27.667751381900253 ,
     27.071123813370523 ,26.743062499999997 ,23.894407498867608 ,27.664505277636977 ,29.339694352319857 ,
     30.046191375670237 ,28.484809652071807 ,28.37639899958421 ,30.228766181045508 ,28.196304026360057 ,
     31.21879166666666 ,30.06345357323231 ,31.247987587835787 ,29.971764405021997 ,32.38483107722503 ,30.8947573668332 ,
     31.538105479034304]
    mpc_err=[0.09388724083903274 ,0.053308639236910586 ,0.08008600585132167 ,0.06707098653286976 ,0.10855095941011209 ,
     0.09465940067812995 ,0.0730002838110344 ,0.08604501831724959 ,0.2121051933827505 ,0.1047444401086048 ,
     0.0237677665634408 ,0.10254878126805424 ,0.06122428740874709 ,0.059364128228642704 ,0.07223327055745098 ,
     0.13864767322378627 ,0.058729656936498606 ,0.059878484600177743 ,0.08033862192268004 ,0.07793566727548316 ,
     0.14065169295981997 ,0.06405072135921865 ,0.07084297608453034 ,0.10719147535991563 ,0.111302340551435 ,
     0.18397568560102517 ,0.11399653772802125 ,0.0902454908334196 ,0.12679441763841434 ,0.13713902642764964 ,
     0.1415422591388269 ,0.14542999492663775 ,0.123505902067684 ,0.1440163044408959 ,0.1356639615397216 ,
     0.10497394349376364 ,0.15170053978408318 ,0.09106748919336996 ,0.07902183585086063 ,0.1404967088856108 ,
     0.21915705071139122 ,0.07819100532289724 ,0.11078545938806754 ,0.07354458271265263 ,0.10881825944642899 ,
     0.10038200875925275 ,0.09319240432491624 ,0.10849147025745909 ,0.08371495838536916 ,0.11623409299797939 ,
     0.07175088376960817 ,0.0690065066364793 ,0.14172551577349055 ,0.1156013710317495 ,0.07536992471746748 ,
     0.08802999288440952 ,0.06927910339580648 ,0.09810112907665737 ,0.06635456180698435 ,0.14678690883506282 ,
     0.07813567333441811 ,0.09376509129179798 ,0.06702066512040285 ,0.08048646049013683 ,0.08341995961077427 ,
     0.08089473218996061 ,0.0894953294630041 ,0.2211506113426717 ,0.08832027203154912 ,0.09096606327923966 ,
     0.0879401666693743 ,0.09261860621702106 ,0.09825788341624225 ,0.09773904599927302 ,0.1506970359070602 ,
     0.1679628090403963 ,0.11393728062001317 ,0.1013909782371722 ,0.14640999133049856 ,0.14057027374685932 ,
     0.11690858001162759 ,0.1177066054364998 ,0.10493831994397548 ,0.21833971278403827 ,0.11580267178476288 ,
     0.13080748083053673 ,0.11837920159212365 ,0.13741998015571152 ,0.1286945193796315 ,0.1494849733626834 ,
     0.13544624911227263 ,0.12866400918431234 ,0.14652512345207658 ,0.12495090712630953 ,0.1335682351648737 ,
     0.14042410004309044 ,0.14544002291277994 ,0.14500170839048135]

    pensieve=[-3.996365914780142e-05 ,0.7613750000000004 ,0.5080442753223872 ,1.0125959257793606 ,1.531937582456153 ,
     2.193624999999999 ,1.5680446537367327 ,2.8120941862485425 ,3.3436545339309807 ,3.3229426347149236 ,
     3.127283242333767 ,3.9581985949248075 ,4.746102689452124 ,4.857174437009837 ,3.910963787622921 ,4.920028310726988 ,
     5.336441965828133 ,5.356556531940271 ,5.901427523233893 ,6.51851975214664 ,4.730743791166993 ,5.913238453199759 ,
     6.392327350119532 ,7.048521235894347 ,8.255885927135996 ,7.310186167719496 ,8.670450873189264 ,9.96196345487883 ,
     10.4374607882826 ,10.08542897354448 ,10.646544669570654 ,10.857038924817568 ,11.488315644069699 ,
     12.937592979341176 ,13.49361316376445 ,14.6767908740527 ,15.123408132417142 ,15.039250051817628 ,
     15.767879366235508 ,15.888214257207236 ,15.922586333733337 ,17.882769643073722 ,18.320792734521355 ,
     19.072165299005913 ,19.687072627914798 ,20.91523069593614 ,20.904354780076037 ,22.20518831284729 ,
     22.060135162882645 ,23.369101161050903 ,24.296333333333333 ,23.364766393478018 ,24.881625000000003 ,
     24.598208333333336 ,25.06368687615874 ,25.465124999999997 ,25.907842128654973 ,25.975375 ,25.9934375 ,
     25.999930884712636 ,26.23233333333333 ,26.428 ,26.355689594217548 ,26.902291666666667 ,27.00704166666667 ,
     27.088562500000002 ,27.327562500000003 ,26.619516234945475 ,27.734104166666665 ,27.624187499999998 ,
     27.449325999961417 ,26.166562869668855 ,27.658705267226743 ,27.788999999999998 ,27.89899343723201 ,
     27.63602348118052 ,27.50267822073528 ,28.65334510724392 ,28.73353076102892 ,28.793296121754956 ,
     30.751317088014588 ,29.563349875429093 ,29.89550062217324 ,28.633608754899715 ,30.867077050532284 ,
     31.775820008066177 ,31.28823939961001 ,31.239559694496542 ,32.34329506802273 ,33.05064310456402 ,
     28.84744517047932 ,32.59111040575911 ,33.6823187566132 ,32.11885956375922 ,32.15067576770711 ,30.900281617919763 ,
     31.714292106953266 ,33.50449558869344]
    pensieve_err=[0.03208019103574333 ,0.0024732526835278385 ,0.06126890913463394 ,0.04508257782693064 ,0.027119284836005893 ,
     0.005055256981125096 ,0.10384157255249613 ,0.0150436072840656 ,0.009651504421287229 ,0.04652499113114961 ,
     0.07688913734195237 ,0.05455598206658783 ,0.020532865974678672 ,0.021769780424292232 ,0.12442532327351867 ,
     0.07327857732958522 ,0.03928729749513142 ,0.06408656197290986 ,0.05023798546001021 ,0.036694551256799 ,
     0.1564075708249508 ,0.11428812320878168 ,0.14811103242299883 ,0.07649086548987234 ,0.06114711679519203 ,
     0.09464640327926879 ,0.1143621409010137 ,0.09934055535801666 ,0.09468528202359679 ,0.07300000895505487 ,
     0.09397655114150234 ,0.09346500857088921 ,0.12675533047812707 ,0.10484083010456385 ,0.09129217031750837 ,
     0.06164907105684478 ,0.06611744396695775 ,0.10965587261895687 ,0.0788406963103774 ,0.11518285944504672 ,
     0.12192153456492363 ,0.08211075361419727 ,0.09291334511234609 ,0.08991706726635557 ,0.09210091078496281 ,
     0.07669030700213346 ,0.0822117513288224 ,0.05648551167915368 ,0.06698716241200584 ,0.07676957228525776 ,
     0.05584374692446419 ,0.06284716632434752 ,0.06097364020003231 ,0.05003621278983936 ,0.06161169663336293 ,
     0.04515218903756839 ,0.04138744107360734 ,0.04129186380600436 ,0.037636138923795116 ,0.06040689469836845 ,
     0.04180908843569363 ,0.045449431140072466 ,0.037423099620281605 ,0.040413239963925464 ,0.04398730291355132 ,
     0.037103742767127565 ,0.030160662477221847 ,0.07295715760678136 ,0.04040954550120386 ,0.046302550797615236 ,
     0.033095103794622674 ,0.16821806663627123 ,0.058708341551326725 ,0.04480634415667366 ,0.10815844081503127 ,
     0.16460628005900868 ,0.16898633805734342 ,0.06581210046685955 ,0.12812913108794974 ,0.11740807078133172 ,
     0.07402394671217379 ,0.10680962703973891 ,0.0790364499764805 ,0.15711074141906312 ,0.08865703262916677 ,
     0.10251364997809856 ,0.09528020417144517 ,0.12222393281984685 ,0.08115863773134692 ,0.08994451439381647 ,
     0.22157690562262414 ,0.11177263841739596 ,0.13534513642879625 ,0.16359581547813173 ,0.16824136315383156 ,
     0.21591965920928996 ,0.20283724249588567 ,0.15096083413675715]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    width = 0.1
    #x = [5, 10, 15, 20]
    x= [ 0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # x = [10 ,20 ,30 ,40 ,50 ,60 ,70 ,80 ,90]
    labels = [ 100, 200, 300, 400, 500, 600, 700, 800, 900]

    x = []
    for i in range( 1, 99 ):
        x.append(i)

    x1 = [p - 0.2 for p in x]
    x2 = [p for p in x]

    # ax.bar(x1, y_train_5, yerr=y_train_5_err, width=0.8,color='red', alpha=0.6, label="train_maxBW_0-2")
    # ax.bar(x2, y_train_20, yerr=y_train_20_err, width=0.8,color='blue', alpha=0.6, label="train_maxBW_0-20")
    ax.bar(x1, pensieve, yerr=pensieve_err, width=0.2,color='green', alpha=0.6, label="pensieve")
    ax.bar(x2, mpc, yerr=mpc_err, width=0.2,color='red', alpha=0.8, label="mpc")
    #ax.bar(x4, mpc, yerr=mpc_err, width=1,color='grey', alpha=0.8, label="mpc")


    # ax.bar( x1 ,y_train_5, color='red' ,alpha=0.6 ,label="train_maxBW_5" )
    # ax.bar( x2 ,y_train_20, color='blue' ,alpha=0.6 ,label="train_maxBW_20" )
    # ax.bar( x3 ,y_train_60, color='orange', alpha=0.6 ,label="train_maxBW_60" )
    # ax.bar( x4 ,y_train_100, color='green', alpha=0.6 ,label="train_maxBW_100" )

    #labels = [[0,2], [0,5], [0,20], [0,60]]

    ax.set_xticks( x )
    # ax.set_xticklabels( labels )

    ax.legend()

    #ax.set_xlim(5,15)
    plt.ylabel('mean reward')
    plt.xlabel('Testing trace maxBW range')
    plt.title('MPC vs Pensieve')
    plt.show()


if __name__ == '__main__':
    main()