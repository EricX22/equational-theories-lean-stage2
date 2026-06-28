% hard3_0136  eq1=1062 eq2=4271  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Y)),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(X,X)) = f(X,f(Y,Z)) )).
