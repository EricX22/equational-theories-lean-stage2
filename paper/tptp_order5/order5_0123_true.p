% order5_0123  eq1=2781 eq2=10951  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(X,Z)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,Z)),f(Z,X))) )).
