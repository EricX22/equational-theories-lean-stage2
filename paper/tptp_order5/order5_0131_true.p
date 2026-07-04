% order5_0131  eq1=15022 eq2=5517  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Z),f(Y,Y)),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(W,f(Y,W))))) )).
