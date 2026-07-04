% order5_0089  eq1=45196 eq2=34797  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,X) = f(Y,f(f(f(Z,Y),W),U)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(f(Z,X),Y)),W) )).
