% order5v2_0781  eq1=17302 eq2=17899  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(W,f(X,Y)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,X),f(Y,f(f(Z,W),Z))) )).
