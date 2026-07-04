% order5v2_1530  eq1=17742 eq2=18486  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(Y,f(Y,Z)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(f(W,X),W))) )).
