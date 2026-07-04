% order5_0018  eq1=30445 eq2=17398  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,f(f(Z,Z),Y))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(Y,f(Z,f(W,Z)))) )).
