% hard3_0193  eq1=1699 eq2=1075  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Y,Z),Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(X,f(X,Y)),X)) )).
