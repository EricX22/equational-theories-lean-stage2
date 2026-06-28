% hard3_0361  eq1=3490 eq2=3471  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(Y,Z),W)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(Y,f(f(X,X),X)) )).
