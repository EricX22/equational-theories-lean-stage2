% hard3_0025  eq1=124 eq2=1776  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(Y,f(f(Y,X),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,Y),X)) )).
