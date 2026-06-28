% hard3_0316  eq1=2927 eq2=3890  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),Z),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(Y,f(Y,Y)),X) )).
