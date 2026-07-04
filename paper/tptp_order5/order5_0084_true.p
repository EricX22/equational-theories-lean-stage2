% order5_0084  eq1=33271 eq2=43555  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(Z,X),X),Y)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(f(Y,Z),f(W,X))) )).
