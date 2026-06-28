% hard3_0252  eq1=2268 eq2=1866  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Y,Y))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,Y)),f(Z,W)) )).
