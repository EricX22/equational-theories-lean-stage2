% order5v2_0413  eq1=27939 eq2=39815  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Y,Z)),X),f(W,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(f(X,f(X,Y)),Z),Y),Y) )).
