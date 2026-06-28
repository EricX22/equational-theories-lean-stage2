% hard3_0080  eq1=618 eq2=3310  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(f(X,Y),Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(X,f(Y,Z))) )).
